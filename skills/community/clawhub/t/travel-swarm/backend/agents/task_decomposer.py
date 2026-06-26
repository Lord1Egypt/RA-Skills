# 必须真实调用，拒绝模拟数据
class TaskDecomposer:
    def __init__(self, amap_client):
        self.amap = amap_client

    async def decompose_and_fetch(self, intent: dict) -> dict:
        city = intent.get("destination", "北京")
        
        # ✅ 修复：优化关键词和types
        try:
            # 景点用更通用的关键词
            scenic_spots = await self.amap.search_poi(keywords="景点", city=city, limit=5)
            
            # 酒店不用types限制（高德types分类可能不准确）
            hotels = await self.amap.search_poi(keywords="酒店", city=city, limit=3)
            
            # 餐厅
            restaurants = await self.amap.search_poi(keywords="餐厅", city=city, limit=3)
            
            print(f"[Decomposer] 景点={len(scenic_spots)}, 酒店={len(hotels)}, 餐厅={len(restaurants)}")
            
        except Exception as e:
            print(f"[Amap Warning] {str(e)}")
            scenic_spots, hotels, restaurants = [], [], []

        return {
            "intent": intent,
            "scenic_spots": scenic_spots,
            "hotels": hotels,
            "restaurants": restaurants
        }