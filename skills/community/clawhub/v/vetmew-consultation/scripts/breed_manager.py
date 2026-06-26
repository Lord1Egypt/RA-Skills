import requests

BREED_JSON_URL = "https://oss-vetmew.vetmew.com/vetmew/pet_breed_ef8a9e.json"

class BreedManager:
    def __init__(self):
        self.breed_data = None
        # 内部映射：1 -> 猫, 2 -> 狗, 3 -> 异宠
        self.type_map = {
            "1": "猫",
            "2": "狗",
            "3": "异宠"
        }

    def load_breeds(self):
        """从 OSS URL 加载品种 JSON 数据"""
        try:
            response = requests.get(BREED_JSON_URL, timeout=10)
            response.raise_for_status()
            self.breed_data = response.json()
            return True
        except Exception as e:
            print(f"加载品种数据失败: {e}")
            return False

    def get_breed_id(self, breed_name, pet_type):
        """
        根据品种名称和宠物类型获取 ID。
        pet_type: "1" (猫), "2" (狗), "3" (异宠)
        """
        if not self.breed_data:
            if not self.load_breeds():
                return None
        
        target_category = self.type_map.get(str(pet_type))
        if not target_category:
            return None

        # 优先完全匹配
        for breed in self.breed_data:
            if breed['name'] == breed_name and breed['category'] == target_category:
                return breed['id']
        
        # 简单模糊匹配（仍需满足分类要求）
        for breed in self.breed_data:
            if (breed_name in breed['name'] or breed['name'] in breed_name) and breed['category'] == target_category:
                return breed['id']
                
        # 匹配不到，按照其他品种
        if pet_type == "1":
            return 454
        if pet_type == "2":
            return 231
        if pet_type == "3":
            return 452  # 异宠通用/其他品种

        return None
