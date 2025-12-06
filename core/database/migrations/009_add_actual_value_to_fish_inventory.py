import sqlite3

def up(cursor: sqlite3.Cursor):
    """
    应用此迁移：为user_fish_inventory表添加actual_value字段。
    """
    logger.debug("正在执行 009_add_actual_value_to_fish_inventory: 为user_fish_inventory表添加actual_value字段...")

    # 为user_fish_inventory表添加actual_value字段
    cursor.execute("""
        ALTER TABLE user_fish_inventory
        ADD COLUMN actual_value INTEGER DEFAULT 0
    """)

    logger.info("009_add_actual_value_to_fish_inventory: actual_value字段已添加到user_fish_inventory表。")

print("成功为user_fish_inventory表添加了actual_value字段")