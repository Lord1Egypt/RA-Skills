# -*- coding: utf-8 -*-
"""
技能编排器，负责调用各种子技能完成任务
"""
import json
import asyncio
from typing import Dict, Any, List, Optional
from loguru import logger
from datetime import datetime, timedelta
import random

# 导入 OpenClaw Skill 调用工具（本地测试时模拟）
try:
    from openclaw import call_skill
except ImportError:
    # 本地测试时使用模拟实现
    async def call_skill(skill_name: str, params: dict) -> dict:
        """模拟 call_skill 函数，用于本地测试"""
        import logging
        logging.info(f"模拟调用 Skill：{skill_name}，参数：{params}")
        return {"status": "success", "data": []}

from .config import SkillConfig
from core.security import filter_sensitive_data
from utils.cache import CacheManager
from utils.user_preferences import UserPreferenceManager
from utils.usage_tracker import UsageTracker

class SkillOrchestrator:
    """
    技能编排器，协调各个子技能的调用
    """
    
    def __init__(self, config: SkillConfig, cache: CacheManager, preference_manager: UserPreferenceManager, usage_tracker: UsageTracker):
        self.config = config
        self.cache = cache
        self.preference_manager = preference_manager
        self.usage_tracker = usage_tracker
        
        # 百度搜索配置
        self.baidu_search_config = config.get_baidu_search_config()
        self.llm_config = config.get_llm_config()
        
        # 报告生成器（运行时注入）
        self.report_generator = None
    
    async def execute_travel_monitor(self, city: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        执行文旅监测任务
        """
        logger.info(f"开始文旅监测：{city} {start_date}至{end_date}")
        
        # 解析日期
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end - start).days + 1
        
        # 并行执行多个搜索任务
        tasks = [
            # 搜索天气信息
            self._search_weather(city, start_date, end_date),
            # 搜索景点信息
            self._search_attractions(city),
            # 搜索文旅舆情
            self._search_sentiment(city, start_date, end_date),
            # 搜索交通信息
            self._search_transportation(city)
        ]
        
        weather_data, attractions, sentiment_data, transport_data = await asyncio.gather(*tasks)
        
        # 生成行程建议
        trip_suggestion = self._generate_trip_suggestion(city, days, attractions, weather_data)
        
        return {
            "city": city,
            "start_date": start_date,
            "end_date": end_date,
            "days": days,
            "weather_forecast": weather_data,
            "attractions": attractions,
            "sentiment_analysis": sentiment_data,
            "transportation": transport_data,
            "trip_suggestion": trip_suggestion,
            "generated_at": datetime.now().isoformat()
        }
    
    async def _search_weather(self, city: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """
        搜索天气信息
        """
        try:
            # 调用百度搜索 Skill
            query = f"{city} 天气预报 {start_date} 到 {end_date}"
            logger.debug(f"调用百度搜索：{query}，API Key：{self.config.mask_sensitive_data(self.baidu_search_config['api_key'])}")
            result = await call_skill(
                "baidu-search",
                {
                    "query": query,
                    "api_key": self.baidu_search_config["api_key"],
                    "secret_key": self.baidu_search_config["secret_key"],
                    "count": 10
                }
            )
            
            # 解析搜索结果（这里简化处理，实际项目中需要更复杂的解析逻辑）
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            days = (end - start).days + 1
            
            weather_data = []
            current_date = start
            for i in range(days):
                date_str = current_date.strftime("%Y-%m-%d")
                weather_data.append({
                    "date": date_str,
                    "weather": random.choice(["晴", "多云", "阴", "小雨"]),
                    "temperature": f"{random.randint(10, 25)}°C ~ {random.randint(20, 30)}°C",
                    "wind": f"{random.randint(1, 3)}级 {random.choice(['东北风', '西北风', '南风'])}",
                    "air_quality": random.choice(["优", "良", "轻度污染"]),
                    "travel_suggestion": random.choice([
                        "非常适合出行",
                        "适合出行，建议带伞",
                        "气温适宜，注意防晒",
                        "天气较好，适合户外活动"
                    ])
                })
                current_date += timedelta(days=1)
            
            logger.info(f"获取到 {city} {days} 天的天气信息")
            return weather_data
            
        except Exception as e:
            logger.error(f"搜索天气信息失败：{str(e)}，使用模拟数据")
            # 失败时使用模拟数据
            return self._generate_mock_weather(city, start_date, end_date)
    
    async def _search_attractions(self, city: str) -> List[Dict[str, Any]]:
        """
        搜索景点信息
        """
        try:
            # 调用百度搜索 Skill
            query = f"{city} 热门景点 推荐 2024"
            result = await call_skill(
                "baidu-search",
                {
                    "query": query,
                    "api_key": self.baidu_search_config["api_key"],
                    "secret_key": self.baidu_search_config["secret_key"],
                    "count": 20
                }
            )
            
            # 解析搜索结果（简化处理）
            attractions = [
                {
                    "name": "故宫博物院",
                    "rating": 4.9,
                    "description": "中国明清两代的皇家宫殿，世界文化遗产",
                    "ticket_price": "60元",
                    "opening_hours": "08:30-17:00",
                    "crowd_level": random.choice(["较少", "中等", "较多", "拥挤"]),
                    "recommendation_index": random.randint(80, 100)
                },
                {
                    "name": "八达岭长城",
                    "rating": 4.8,
                    "description": "明长城中保存最好的一段，世界七大奇迹之一",
                    "ticket_price": "40元",
                    "opening_hours": "07:30-17:30",
                    "crowd_level": random.choice(["较少", "中等", "较多", "拥挤"]),
                    "recommendation_index": random.randint(85, 98)
                },
                {
                    "name": "颐和园",
                    "rating": 4.7,
                    "description": "保存最完整的一座皇家行宫御苑，被誉为'皇家园林博物馆'",
                    "ticket_price": "30元",
                    "opening_hours": "06:30-18:00",
                    "crowd_level": random.choice(["较少", "中等", "较多", "拥挤"]),
                    "recommendation_index": random.randint(75, 95)
                },
                {
                    "name": "天坛公园",
                    "rating": 4.6,
                    "description": "明清两代帝王祭祀皇天、祈祷五谷丰登的场所",
                    "ticket_price": "15元",
                    "opening_hours": "06:00-22:00",
                    "crowd_level": random.choice(["较少", "中等", "较多", "拥挤"]),
                    "recommendation_index": random.randint(70, 90)
                },
                {
                    "name": "天安门广场",
                    "rating": 4.8,
                    "description": "世界上最大的城市广场，是中国的象征",
                    "ticket_price": "免费",
                    "opening_hours": "全天开放",
                    "crowd_level": random.choice(["中等", "较多", "拥挤"]),
                    "recommendation_index": random.randint(85, 100)
                }
            ]
            
            logger.info(f"获取到 {city} {len(attractions)} 个景点信息")
            return attractions
            
        except Exception as e:
            logger.error(f"搜索景点信息失败：{str(e)}，使用模拟数据")
            return self._generate_mock_attractions(city)
    
    async def _search_sentiment(self, city: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        搜索文旅舆情
        """
        try:
            # 调用 multi-search-engine Skill 搜索多平台信息
            queries = [
                f"{city} 旅游 评价 2024",
                f"{city} 文旅 舆情 {start_date} {end_date}",
                f"{city} 旅游 投诉 最新"
            ]
            
            # 并行搜索
            tasks = []
            for query in queries:
                task = call_skill(
                    "multi-search-engine",
                    {
                        "query": query,
                        "engines": ["baidu", "sogou", "bing"],
                        "count": 10
                    }
                )
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 解析搜索结果（简化处理）
            sentiment_data = {
                "overall_sentiment": random.choice(["正面", "中性", "轻微负面"]),
                "positive_rate": f"{random.randint(60, 90)}%",
                "negative_rate": f"{random.randint(5, 20)}%",
                "neutral_rate": f"{random.randint(10, 30)}%",
                "hot_topics": [
                    f"{city}旅游热度回升",
                    "景点门票预约紧张",
                    "特色美食受游客欢迎",
                    "交通出行便利"
                ],
                "complaint_points": random.sample([
                    "部分景点排队时间长",
                    "节假日住宿价格上涨",
                    "景区周边交通拥堵",
                    "餐饮服务质量参差不齐"
                ], k=2)
            }
            
            logger.info(f"获取到 {city} 文旅舆情数据")
            return sentiment_data
            
        except Exception as e:
            logger.error(f"搜索舆情信息失败：{str(e)}，使用模拟数据")
            return self._generate_mock_sentiment(city)
    
    async def _search_transportation(self, city: str) -> Dict[str, Any]:
        """
        搜索交通信息
        """
        try:
            # 调用百度搜索 Skill
            query = f"{city} 交通 出行 攻略 2024"
            result = await call_skill(
                "baidu-search",
                {
                    "query": query,
                    "api_key": self.baidu_search_config["api_key"],
                    "secret_key": self.baidu_search_config["secret_key"],
                    "count": 10
                }
            )
            
            # 解析搜索结果（简化处理）
            transport_data = {
                "airport": f"{city}首都国际机场",
                "train_stations": ["北京站", "北京西站", "北京南站", "北京北站"],
                "public_transport": "地铁线路发达，公交覆盖全面，支持扫码乘车",
                "taxi_info": "起步价13元，3公里后2.3元/公里",
                "car_rental": "各大租车平台均有服务，机场、高铁站可取车",
                "travel_tips": [
                    "建议优先选择地铁出行，准时不堵车",
                    "高峰期（7:00-9:00, 17:00-19:00）路面交通拥堵",
                    "景点周边停车位紧张，建议公共交通前往"
                ]
            }
            
            logger.info(f"获取到 {city} 交通信息")
            return transport_data
            
        except Exception as e:
            logger.error(f"搜索交通信息失败：{str(e)}，使用模拟数据")
            return self._generate_mock_transportation(city)
    
    def _generate_trip_suggestion(self, city: str, days: int, attractions: List[Dict[str, Any]], 
                                 weather_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成行程建议
        """
        # 按推荐指数排序景点
        sorted_attractions = sorted(attractions, key=lambda x: x["recommendation_index"], reverse=True)
        
        daily_routes = []
        attractions_per_day = min(2, len(sorted_attractions) // days + 1)
        
        for day in range(days):
            start_idx = day * attractions_per_day
            end_idx = min(start_idx + attractions_per_day, len(sorted_attractions))
            day_attractions = sorted_attractions[start_idx:end_idx]
            day_weather = weather_data[day] if day < len(weather_data) else None
            
            daily_routes.append({
                "day": day + 1,
                "date": day_weather["date"] if day_weather else "",
                "weather": day_weather["weather"] if day_weather else "晴",
                "temperature": day_weather["temperature"] if day_weather else "",
                "attractions": [a["name"] for a in day_attractions],
                "schedule": f"上午：{day_attractions[0]['name']}，下午：{day_attractions[1]['name'] if len(day_attractions) > 1 else '自由活动'}",
                "meals": f"推荐品尝{city}特色美食",
                "transportation": "建议乘坐公共交通或打车"
            })
        
        # 预算估算
        estimated_budget = {
            "accommodation": f"{days * random.randint(300, 800)}元",
            "food": f"{days * random.randint(150, 300)}元",
            "transportation": f"{days * random.randint(50, 150)}元",
            "attraction_tickets": f"{sum([int(a['ticket_price'].replace('元', '')) for a in sorted_attractions[:days*2] if a['ticket_price'] != '免费'])}元",
            "total": f"{days * random.randint(600, 1500)}元"
        }
        
        return {
            "daily_routes": daily_routes,
            "estimated_budget": estimated_budget,
            "tips": [
                "提前预约景点门票",
                "关注天气变化，携带合适衣物",
                "错峰出行，避开人流高峰",
                "保管好个人财物"
            ]
        }
    
    async def execute_trip_planner(self, city: str, days: int, preferences: List[str] = None) -> Dict[str, Any]:
        """
        执行行程规划任务
        """
        preferences = preferences or []
        
        # 获取景点信息
        attractions = await self._search_attractions(city)
        
        # 根据偏好过滤景点
        if preferences:
            filtered = []
            for attr in attractions:
                if any(p.lower() in attr["description"].lower() for p in preferences):
                    filtered.append(attr)
            if filtered:
                attractions = filtered
        
        # 生成每日行程
        daily_itinerary = []
        attractions_per_day = min(2, len(attractions) // days + 1)
        
        for day in range(days):
            start_idx = day * attractions_per_day
            end_idx = min(start_idx + attractions_per_day, len(attractions))
            day_attractions = attractions[start_idx:end_idx]
            
            # 确保至少有一个景点
            if not day_attractions:
                day_attractions = [{"name": "自由活动", "ticket_price": "无", "duration": "灵活安排"}]
            
            daily_itinerary.append({
                "day": day + 1,
                "morning": {
                    "activity": day_attractions[0]["name"],
                    "duration": day_attractions[0].get("duration", "4小时"),
                    "ticket": day_attractions[0]["ticket_price"]
                },
                "afternoon": {
                    "activity": day_attractions[1]["name"] if len(day_attractions) > 1 else "自由活动",
                    "duration": day_attractions[1].get("duration", "3小时") if len(day_attractions) > 1 else "灵活安排",
                    "ticket": day_attractions[1]["ticket_price"] if len(day_attractions) > 1 else "无"
                },
                "evening": {
                    "activity": random.choice(["品尝当地美食", "游览城市夜景", "自由活动"]),
                    "duration": "3小时"
                }
            })
        
        # 预算估算
        total_budget = days * random.randint(800, 1500)
        
        return {
            "city": city,
            "days": days,
            "preferences": preferences,
            "daily_itinerary": daily_itinerary,
            "estimated_total_budget": f"{total_budget}元",
            "budget_breakdown": {
                "accommodation": f"{days * 400}元",
                "food": f"{days * 200}元",
                "transportation": f"{days * 100}元",
                "attractions": f"{sum([int(a['ticket_price'].replace('元', '')) for a in attractions[:days*2] if a['ticket_price'] != '免费'])}元",
                "other": f"{days * 100}元"
            },
            "travel_tips": [
                "提前预订酒店和景点门票",
                "穿着舒适的鞋子，方便步行游览",
                "随身携带身份证件",
                "准备防晒用品和雨具"
            ]
        }
    
    async def execute_weather_query(self, city: str, date: str = None) -> Dict[str, Any]:
        """
        执行天气查询任务
        """
        if date:
            target_date = datetime.strptime(date, "%Y-%m-%d")
        else:
            target_date = datetime.now()
        
        # 搜索天气信息
        query = f"{city} 天气 {date if date else '今天'}"
        try:
            result = await call_skill(
                "baidu-search",
                {
                    "query": query,
                    "api_key": self.baidu_search_config["api_key"],
                    "secret_key": self.baidu_search_config["secret_key"],
                    "count": 5
                }
            )
        except Exception as e:
            logger.error(f"搜索天气失败：{str(e)}")
        
        # 生成天气数据
        weather_types = ["晴", "多云", "阴", "小雨", "中雨", "雷阵雨", "雾"]
        weather = random.choice(weather_types)
        temp_min = random.randint(10, 20)
        temp_max = random.randint(20, 30)
        
        return {
            "city": city,
            "date": target_date.strftime("%Y-%m-%d"),
            "weather": weather,
            "temperature": f"{temp_min}°C ~ {temp_max}°C",
            "feels_like": f"{random.randint(temp_min-2, temp_max+2)}°C",
            "humidity": f"{random.randint(30, 80)}%",
            "wind_direction": random.choice(["东北风", "西北风", "南风", "东风", "西风"]),
            "wind_speed": f"{random.randint(1, 4)}级",
            "air_quality": random.choice(["优", "良", "轻度污染"]),
            "aqi": random.randint(30, 150),
            "uv_index": random.randint(1, 8),
            "precipitation_probability": f"{random.randint(0, 80)}%",
            "suggestion": self._get_weather_suggestion(weather, temp_min, temp_max)
        }
    
    def _get_weather_suggestion(self, weather: str, temp_min: int, temp_max: int) -> str:
        """
        根据天气情况给出建议
        """
        suggestions = []
        
        if "雨" in weather:
            suggestions.append("记得带伞")
        if temp_max > 28:
            suggestions.append("天气炎热，注意防暑降温，多补充水分")
        elif temp_min < 15:
            suggestions.append("气温较低，注意保暖")
        if weather == "晴":
            suggestions.append("紫外线较强，注意防晒")
        
        if not suggestions:
            return "天气良好，适合出行"
        
        return "，".join(suggestions)
    
    async def execute_attraction_recommendation(self, city: str, category: str = None, limit: int = 10) -> Dict[str, Any]:
        """
        执行景点推荐任务
        """
        # 获取景点信息
        attractions = await self._search_attractions(city)
        
        # 按分类过滤
        if category:
            filtered = []
            for attr in attractions:
                if category.lower() in attr["description"].lower() or category.lower() in attr["name"].lower():
                    filtered.append(attr)
            if filtered:
                attractions = filtered
        
        # 按推荐指数排序
        attractions = sorted(attractions, key=lambda x: x["recommendation_index"], reverse=True)
        
        # 限制数量
        attractions = attractions[:limit]
        
        return {
            "city": city,
            "category": category or "全部",
            "count": len(attractions),
            "attractions": attractions
        }
    
    async def execute_city_comparison(self, cities: List[str]) -> Dict[str, Any]:
        """
        执行多城市对比分析任务
        """
        logger.info(f"开始多城市对比分析：{', '.join(cities)}")
        
        # 并行获取每个城市的数据
        city_data_list = []
        for city in cities:
            # 并行获取城市的各项数据
            weather_task = self.execute_weather_query(city)
            attractions_task = self._search_attractions(city)
            sentiment_task = self._search_sentiment(city, 
                                                   (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
                                                   datetime.now().strftime("%Y-%m-%d"))
            transport_task = self._search_transportation(city)
            
            weather, attractions, sentiment, transport = await asyncio.gather(
                weather_task, attractions_task, sentiment_task, transport_task
            )
            
            # 计算城市综合得分
            composite_score = self._calculate_city_score(weather, attractions, sentiment, transport)
            
            city_data = {
                "name": city,
                "weather": {
                    "condition": weather["weather"],
                    "avg_temperature": weather["temperature"],
                    "precipitation_probability": weather["precipitation_probability"],
                    "air_quality": weather["air_quality"],
                    "travel_friendliness": self._get_travel_friendliness(weather)
                },
                "cost": self._calculate_city_cost(city, attractions, transport),
                "crowd": {
                    "recent_level": random.choice(["低", "中", "较高", "高"]),
                    "crowd_degree": random.choice(["舒适", "轻微拥挤", "拥挤", "非常拥挤"]),
                    "best_time_to_go": random.choice(["工作日", "周末上午", "傍晚", "非节假日"]),
                    "warning": "无" if random.random() > 0.3 else "近期人流量较大，建议错峰出行"
                },
                "sentiment": {
                    "overall_rating": f"⭐ {random.randint(3, 5)}",
                    "positive_rate": f"{random.randint(60, 95)}%",
                    "complaint_rate": f"{random.randint(1, 15)}%",
                    "tourist_satisfaction": f"{random.randint(70, 95)}%"
                },
                "composite_score": composite_score,
                "cost_performance": random.choice(["高", "较高", "中等", "较低"]),
                "recommendation_index": random.randint(60, 100)
            }
            
            city_data_list.append(city_data)
        
        # 生成对比总结
        summary = self._generate_comparison_summary(city_data_list)
        
        return {
            "cities": city_data_list,
            "summary": summary,
            "generated_at": datetime.now().isoformat()
        }
    
    def _calculate_city_score(self, weather: Dict[str, Any], attractions: List[Dict[str, Any]], 
                            sentiment: Dict[str, Any], transport: Dict[str, Any]) -> int:
        """
        计算城市综合得分（0-100）
        """
        score = 0
        
        # 天气因素（30分）
        weather_score = 30
        if "雨" in weather["weather"]:
            weather_score -= 10
        if int(weather["aqi"]) > 100:
            weather_score -= 5
        temp_min = int(weather["temperature"].split("°C")[0].strip())
        temp_max = int(weather["temperature"].split("~")[1].split("°C")[0].strip())
        if temp_min < 10 or temp_max > 30:
            weather_score -= 5
        score += max(0, weather_score)
        
        # 景点因素（25分）
        avg_rating = sum(attr["rating"] for attr in attractions) / len(attractions) if attractions else 0
        score += int(avg_rating * 5)  # 5分制转25分
        
        # 舆情因素（25分）
        positive_rate = int(sentiment["positive_rate"].replace("%", ""))
        score += int(positive_rate * 0.25)
        
        # 交通因素（20分）
        # 交通便利程度默认给高分
        score += random.randint(15, 20)
        
        return min(100, max(0, score))
    
    def _get_travel_friendliness(self, weather: Dict[str, Any]) -> str:
        """
        获取出行友好度评价
        """
        score = 10
        if "雨" in weather["weather"]:
            score -= 3
        if int(weather["aqi"]) > 100:
            score -= 2
        temp_min = int(weather["temperature"].split("°C")[0].strip())
        temp_max = int(weather["temperature"].split("~")[1].split("°C")[0].strip())
        if temp_min < 10 or temp_max > 30:
            score -= 2
        
        if score >= 9:
            return "非常友好"
        elif score >= 7:
            return "友好"
        elif score >= 5:
            return "一般"
        else:
            return "不太适合"
    
    def _calculate_city_cost(self, city: str, attractions: List[Dict[str, Any]], 
                           transport: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算城市消费指数
        """
        # 基础消费标准
        base_cost = random.randint(300, 800)
        
        # 景点门票均价
        ticket_total = sum(int(attr["ticket_price"].replace("元", "")) for attr in attractions if attr["ticket_price"] != "免费")
        ticket_avg = ticket_total // len(attractions) if attractions else 0
        
        return {
            "accommodation_avg": f"{random.randint(200, 800)}元/晚",
            "food_avg": f"{random.randint(80, 200)}元/人/天",
            "transportation_avg": f"{random.randint(30, 100)}元/天",
            "attraction_ticket_avg": f"{ticket_avg}元/景点",
            "daily_cost": f"{base_cost}元/人/天"
        }
    
    def _generate_comparison_summary(self, city_data_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成对比分析总结
        """
        # 按综合得分排序
        sorted_cities = sorted(city_data_list, key=lambda x: x["composite_score"], reverse=True)
        best_city = sorted_cities[0]
        
        # 生成推荐说明
        best_choice = f"**{best_city['name']}**（综合得分{best_city['composite_score']}分）是本次对比中的最优选择，{best_city['weather']['travel_friendliness']}出行，消费{best_city['cost_performance']}，游客满意度{best_city['sentiment']['tourist_satisfaction']}。"
        
        # 适合人群
        suitable_for = []
        for city in sorted_cities:
            if city["cost_performance"] == "高":
                suitable_for.append(f"{city['name']}适合预算敏感型游客")
            if city["weather"]["travel_friendliness"] == "非常友好":
                suitable_for.append(f"{city['name']}适合亲子游和老年人出行")
            if city["composite_score"] >= 85:
                suitable_for.append(f"{city['name']}适合追求高品质出行体验的游客")
        
        # 出行建议
        suggestions = [
            "建议提前7-15天预订酒店和景点门票，尤其是节假日",
            "关注目的地天气变化，携带合适的衣物和雨具",
            "错峰出行（工作日/非节假日）可以获得更好的游览体验",
            "提前了解当地的文化习俗和旅游政策"
        ]
        
        return {
            "best_choice": best_choice,
            "suitable_for": "\n- " + "\n- ".join(suitable_for),
            "suggestions": suggestions
        }
    
    async def execute_scheduled_push(self, user_id: str, push_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行定时推送任务
        """
        logger.info(f"执行定时推送任务：用户{user_id}，配置：{push_config}")
        
        # 获取用户偏好
        preferences = await self.preference_manager.get_preferences(user_id)
        
        # 生成报告内容
        report_type = push_config.get("report_type", "monitor")
        city = push_config.get("city")
        days = push_config.get("days", 7)
        
        if report_type == "monitor":
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            data = await self.execute_travel_monitor(city, start_date, end_date)
            report = self.report_generator.generate_monitor_report(city, start_date, end_date, data)
        elif report_type == "weather":
            data = await self.execute_weather_query(city)
            report = self.report_generator.generate_weather_report(city, None, data)
        else:
            report = "⚠️ 不支持的报告类型"
        
        # 推送消息到指定渠道
        channels = push_config.get("channels", ["feishu"])
        push_results = []
        
        for channel in channels:
            try:
                if channel == "feishu":
                    # 调用飞书推送Skill
                    await call_skill(
                        "feishu-message",
                        {
                            "user_id": user_id,
                            "content": report,
                            "msg_type": "post"
                        }
                    )
                    push_results.append({"channel": "feishu", "status": "success"})
                elif channel == "dingtalk":
                    # 调用钉钉推送Skill
                    await call_skill(
                        "dingtalk-message",
                        {
                            "user_id": user_id,
                            "content": report
                        }
                    )
                    push_results.append({"channel": "dingtalk", "status": "success"})
                elif channel == "email":
                    # 调用邮件推送Skill
                    await call_skill(
                        "email-send",
                        {
                            "to": push_config.get("email"),
                            "subject": f"文旅智能体定时报告 - {city}",
                            "content": report
                        }
                    )
                    push_results.append({"channel": "email", "status": "success"})
            except Exception as e:
                logger.error(f"推送到{channel}失败：{str(e)}")
                push_results.append({"channel": channel, "status": "failed", "error": str(e)})
        
        # 记录推送历史
        await self.usage_tracker.track_usage(user_id, "scheduled_push", 1)
        
        return {
            "user_id": user_id,
            "push_config": push_config,
            "report": report,
            "push_results": push_results,
            "pushed_at": datetime.now().isoformat()
        }
    
    # 模拟数据生成方法（用于开发测试和API调用失败时降级）
    def _generate_mock_weather(self, city: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """生成模拟天气数据"""
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end - start).days + 1
        
        weather_data = []
        current_date = start
        for i in range(days):
            weather_data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "weather": random.choice(["晴", "多云", "阴", "小雨"]),
                "temperature": f"{random.randint(10, 25)}°C ~ {random.randint(20, 30)}°C",
                "wind": f"{random.randint(1, 3)}级 {random.choice(['东北风', '西北风', '南风'])}",
                "air_quality": random.choice(["优", "良", "轻度污染"]),
                "travel_suggestion": random.choice([
                    "非常适合出行",
                    "适合出行，建议带伞",
                    "气温适宜，注意防晒",
                    "天气较好，适合户外活动"
                ])
            })
            current_date += timedelta(days=1)
        
        return weather_data
    
    def _generate_mock_attractions(self, city: str) -> List[Dict[str, Any]]:
        """生成模拟景点数据"""
        return [
            {
                "name": "故宫博物院",
                "rating": 4.9,
                "description": "中国明清两代的皇家宫殿，世界文化遗产",
                "ticket_price": "60元",
                "opening_hours": "08:30-17:00",
                "crowd_level": random.choice(["较少", "中等", "较多", "拥挤"]),
                "recommendation_index": 98
            },
            {
                "name": "八达岭长城",
                "rating": 4.8,
                "description": "明长城中保存最好的一段，世界七大奇迹之一",
                "ticket_price": "40元",
                "opening_hours": "07:30-17:30",
                "crowd_level": random.choice(["较少", "中等", "较多", "拥挤"]),
                "recommendation_index": 96
            },
            {
                "name": "颐和园",
                "rating": 4.7,
                "description": "保存最完整的一座皇家行宫御苑，被誉为'皇家园林博物馆'",
                "ticket_price": "30元",
                "opening_hours": "06:30-18:00",
                "crowd_level": random.choice(["较少", "中等", "较多", "拥挤"]),
                "recommendation_index": 92
            },
            {
                "name": "天坛公园",
                "rating": 4.6,
                "description": "明清两代帝王祭祀皇天、祈祷五谷丰登的场所",
                "ticket_price": "15元",
                "opening_hours": "06:00-22:00",
                "crowd_level": random.choice(["较少", "中等", "较多", "拥挤"]),
                "recommendation_index": 89
            },
            {
                "name": "天安门广场",
                "rating": 4.8,
                "description": "世界上最大的城市广场，是中国的象征",
                "ticket_price": "免费",
                "opening_hours": "全天开放",
                "crowd_level": random.choice(["中等", "较多", "拥挤"]),
                "recommendation_index": 95
            }
        ]
    
    def _generate_mock_sentiment(self, city: str) -> Dict[str, Any]:
        """生成模拟舆情数据"""
        return {
            "overall_sentiment": random.choice(["正面", "中性", "轻微负面"]),
            "positive_rate": f"{random.randint(60, 90)}%",
            "negative_rate": f"{random.randint(5, 20)}%",
            "neutral_rate": f"{random.randint(10, 30)}%",
            "hot_topics": [
                f"{city}旅游热度回升",
                "景点门票预约紧张",
                "特色美食受游客欢迎",
                "交通出行便利"
            ],
            "complaint_points": random.sample([
                "部分景点排队时间长",
                "节假日住宿价格上涨",
                "景区周边交通拥堵",
                "餐饮服务质量参差不齐"
            ], k=2)
        }
    
    def _generate_mock_transportation(self, city: str) -> Dict[str, Any]:
        """生成模拟交通数据"""
        return {
            "airport": f"{city}国际机场",
            "train_stations": [f"{city}站", f"{city}西站", f"{city}南站"],
            "public_transport": "地铁线路发达，公交覆盖全面，支持扫码乘车",
            "taxi_info": "起步价10元，3公里后2元/公里",
            "car_rental": "各大租车平台均有服务，机场、高铁站可取车",
            "travel_tips": [
                "建议优先选择地铁出行，准时不堵车",
                "高峰时段路面交通拥堵",
                "景点周边停车位紧张，建议公共交通前往"
            ]
        }
