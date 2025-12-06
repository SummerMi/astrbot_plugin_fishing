import random
import numpy as np
import matplotlib.pyplot as plt
import json

# 模拟当前的稀有度加成逻辑
def simulate_rarity_distribution(zone_id=3, rare_chance=0.1, iterations=100000):
    # 区域稀有度分布（与fishing_service.py中的设置一致）
    rarity_weights = {
        1: [0.75, 0.15, 0.07, 0.02, 0.01],  # 区域1：强正偏
        2: [0.38, 0.30, 0.18, 0.10, 0.04],  # 区域2：中等正偏
        3: [0.20, 0.25, 0.25, 0.20, 0.10]   # 区域3：弱正偏/微负偏
    }
    
    current_weights = rarity_weights.get(zone_id, rarity_weights[1])
    rarity_distribution = current_weights.copy()
    
    # 原始分布（无加成）
    original_distribution = rarity_distribution.copy()
    
    # 应用稀有度加成（实现负偏效果）
    if rare_chance > 0.0:
        # 为不同稀有度设置不同的加成系数，高稀有度获得更高的加成
        MAX_RARE_CHANCE = 0.3
        NON_LINEAR_POWER = 2.0  # 核心参数：设置为 2.0 实现平方增长
        TARGET_MULTIPLIERS = [0.0, 0.10, 0.50, 1.00, 2.00]
        # 计算各稀有度的实际加成
        normalized_rare_chance = rare_chance / MAX_RARE_CHANCE
        non_linear_scale = normalized_rare_chance ** NON_LINEAR_POWER 
        
        # 2. 应用非线性加权
        rarity_distribution = [
            x * (1 + non_linear_scale * TARGET_MULTIPLIERS[i])
            for i, x in enumerate(rarity_distribution)
        ]
                
        # 3. 归一化概率分布
        total = sum(rarity_distribution)
        rarity_distribution = [x / total for x in rarity_distribution]
    
    # 模拟钓鱼结果
    rarity_levels = [1, 2, 3, 4, 5]
    original_results = random.choices(rarity_levels, weights=original_distribution, k=iterations)
    new_results = random.choices(rarity_levels, weights=rarity_distribution, k=iterations)
    
    return original_distribution, rarity_distribution, original_results, new_results

# 计算分布的偏度
def calculate_skewness(results):
    return np.mean((results - np.mean(results)) ** 3) / (np.std(results) ** 3)

# 生成统计信息
def generate_statistics(results, distribution):
    counts = [results.count(1), results.count(2), results.count(3), results.count(4), results.count(5)]
    percentages = [count / len(results) for count in counts]
    
    stats = {
        "counts": counts,
        "percentages": percentages,
        "mean": np.mean(results),
        "median": np.median(results),
        "std": np.std(results),
        "skewness": calculate_skewness(results),
        "distribution": distribution
    }
    
    return stats

# 可视化分布
def visualize_distribution(original_stats, new_stats, rare_chance):
    rarity_levels = [1, 2, 3, 4, 5]
    
    # 创建图形
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 原始分布条形图
    axes[0, 0].bar(rarity_levels, original_stats["counts"], color='skyblue')
    axes[0, 0].set_title(f'原始稀有度分布（稀有度加成：{rare_chance}）')
    axes[0, 0].set_xlabel('稀有度')
    axes[0, 0].set_ylabel('出现次数')
    axes[0, 0].set_xticks(rarity_levels)
    
    # 新分布条形图
    axes[0, 1].bar(rarity_levels, new_stats["counts"], color='lightcoral')
    axes[0, 1].set_title(f'应用加成后的稀有度分布（稀有度加成：{rare_chance}）')
    axes[0, 1].set_xlabel('稀有度')
    axes[0, 1].set_ylabel('出现次数')
    axes[0, 1].set_xticks(rarity_levels)
    
    # 概率分布比较
    width = 0.35
    x = np.arange(len(rarity_levels))
    axes[1, 0].bar(x - width/2, original_stats["percentages"], width, label='原始分布')
    axes[1, 0].bar(x + width/2, new_stats["percentages"], width, label='新分布')
    axes[1, 0].set_title(f'稀有度概率分布比较（稀有度加成：{rare_chance}）')
    axes[1, 0].set_xlabel('稀有度')
    axes[1, 0].set_ylabel('概率')
    axes[1, 0].set_xticks(x)
    axes[1, 0].set_xticklabels(rarity_levels)
    axes[1, 0].legend()
    
    # 偏度变化
    skewness = [original_stats["skewness"], new_stats["skewness"]]
    labels = ['原始分布', '新分布']
    axes[1, 1].bar(labels, skewness, color=['skyblue', 'lightcoral'])
    axes[1, 1].set_title(f'分布偏度比较（稀有度加成：{rare_chance}）')
    axes[1, 1].set_ylabel('偏度值')
    axes[1, 1].axhline(y=0, color='black', linestyle='--', alpha=0.3)
    
    # 添加统计信息文本
    text = f"""
    原始分布统计：
    均值: {original_stats['mean']:.4f}
    中位数: {original_stats['median']:.4f}
    标准差: {original_stats['std']:.4f}
    偏度: {original_stats['skewness']:.4f}
    
    新分布统计：
    均值: {new_stats['mean']:.4f}
    中位数: {new_stats['median']:.4f}
    标准差: {new_stats['std']:.4f}
    偏度: {new_stats['skewness']:.4f}
    """
    
    plt.figtext(0.5, 0.01, text, ha="center", fontsize=10)
    plt.tight_layout()
    
    # 保存图表
    plt.savefig(f'rarity_distribution_comparison_{rare_chance}.png')
    plt.close()

# 主函数
def main():
    zone_id = 3  # 使用区域3作为测试
    rare_chances = [0.05, 0.1, 0.2, 0.3]  # 测试不同的稀有度加成值
    iterations = 100000  # 模拟次数
    
    results = {}
    
    for rare_chance in rare_chances:
        print(f"正在模拟稀有度加成: {rare_chance}...")
        
        # 执行模拟
        original_dist, new_dist, original_results, new_results = simulate_rarity_distribution(
            zone_id=zone_id, 
            rare_chance=rare_chance, 
            iterations=iterations
        )
        
        # 生成统计信息
        original_stats = generate_statistics(original_results, original_dist)
        new_stats = generate_statistics(new_results, new_dist)
        
        # 保存结果
        results[rare_chance] = {
            "original": original_stats,
            "new": new_stats
        }
        
        # 可视化分布
        visualize_distribution(original_stats, new_stats, rare_chance)
        
        # 打印统计信息
        print(f"\n稀有度加成: {rare_chance}")
        print(f"原始分布 - 均值: {original_stats['mean']:.4f}, 偏度: {original_stats['skewness']:.4f}")
        print(f"新分布 - 均值: {new_stats['mean']:.4f}, 偏度: {new_stats['skewness']:.4f}")
        print(f"偏度变化: {new_stats['skewness'] - original_stats['skewness']:.4f}")
        
        # 打印各稀有度的概率变化
        print(f"\n各稀有度概率变化:")
        print(f"稀有度 | 原始概率 | 新概率 | 变化")
        print(f"-------|----------|--------|------")
        for i in range(5):
            original_p = original_stats['percentages'][i]
            new_p = new_stats['percentages'][i]
            change = new_p - original_p
            print(f"{i+1:5d} | {original_p:8.4f} | {new_p:6.4f} | {change:6.4f}")
    
    # 保存结果到JSON文件
    with open('rarity_bonus_simulation_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n模拟完成！结果已保存到 rarity_bonus_simulation_results.json")
    print(f"图表已保存到 rarity_distribution_comparison_*.png")

if __name__ == "__main__":
    main()