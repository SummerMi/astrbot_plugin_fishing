from draw import backpack


class TestBackpack:
    def test_draw_backpack_image_show_coins(self):
        user_data = {
            "user_id": 1234567890,
            "nickname": "Shadow",
            "rods": [],
            "accessories": [],
            "baits": [],
            "coins": 123455615198488498489498498498489498678910,
        }
        image = backpack.draw_backpack_image(user_data)
        # image.save("test_draw_backpack_image_show_coins.png")
