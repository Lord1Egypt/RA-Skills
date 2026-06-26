# -*- coding: utf-8 -*-
"""
报告生成模块，根据数据生成各种格式的报告
"""
from typing import Dict, Any, List
from datetime import datetime
from loguru import logger

from .config import SkillConfig

class ReportGenerator:
    """
    报告生成器，支持生成各种类型的文旅报告
    """
    
    def __init__(self, config: SkillConfig):
        self.config = config
        self.language = config.default_language
    
    def generate_monitor_report(self, city: str, start_date: str, end_date: str, data: Dict[str, Any]) -> str:
        """
        生成文旅监测报告（Markdown格式）
        """
        logger.info(f"生成文旅监测报告：{city} {start_date}至{end_date}")
        
        # 计算天数
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days = (end - start).days + 1
        
        # 生成报告内容
        report = f"""# 📊 {city} 文旅监测报告
**监测时间**：{start_date} 至 {end_date}（共 {days} 天）
**生成时间**：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 🌤️ 天气预报
| 日期 | 天气 | 温度 | 风力 | 空气质量 | 出行建议 |
|------|------|------|------|----------|----------|
"""
        
        # 添加天气数据
        for weather in data.get("weather_forecast", []):
            report += f"| {weather['date']} | {weather['weather']} | {weather['temperature']} | {weather['wind']} | {weather['air_quality']} | {weather['travel_suggestion']} |\n"
        
        # 景点信息
        report += """
---

## 🏯 热门景点信息
| 景点名称 | 评分 | 门票价格 | 开放时间 | 人流量 | 推荐指数 |
|----------|------|----------|----------|--------|----------|
"""
        
        attractions = sorted(data.get("attractions", []), key=lambda x: x["recommendation_index"], reverse=True)
        for attr in attractions[:8]:  # 显示前8个景点
            report += f"| {attr['name']} | ⭐ {attr['rating']} | {attr['ticket_price']} | {attr['opening_hours']} | {attr['crowd_level']} | {attr['recommendation_index']} |\n"
        
        # 舆情分析
        sentiment = data.get("sentiment_analysis", {})
        report += f"""
---

## 📈 舆情分析
**整体评价**：{sentiment.get('overall_sentiment', '中性')}
**正面评价占比**：{sentiment.get('positive_rate', '70%')}
**负面评价占比**：{sentiment.get('negative_rate', '10%')}
**中立评价占比**：{sentiment.get('neutral_rate', '20%')}

### 🔥 热门话题
"""
        for topic in sentiment.get("hot_topics", []):
            report += f"- ✅ {topic}\n"
        
        report += """
### ⚠️ 投诉热点
"""
        for complaint in sentiment.get("complaint_points", []):
            report += f"- ❌ {complaint}\n"
        
        # 交通信息
        transport = data.get("transportation", {})
        report += f"""
---

## 🚗 交通出行
**机场**：{transport.get('airport', '无数据')}
**火车站**：{'、'.join(transport.get('train_stations', ['无数据']))}
**公共交通**：{transport.get('public_transport', '无数据')}
**出租车信息**：{transport.get('taxi_info', '无数据')}
**租车服务**：{transport.get('car_rental', '无数据')}

### 💡 出行建议
"""
        for tip in transport.get("travel_tips", []):
            report += f"- {tip}\n"
        
        # 行程建议
        trip_suggestion = data.get("trip_suggestion", {})
        budget = trip_suggestion.get("estimated_budget", {})
        report += f"""
---

## 🗺️ 行程建议
### 每日行程推荐
"""
        
        for route in trip_suggestion.get("daily_routes", []):
            report += f"""
#### 📅 第 {route['day']} 天（{route['date']}）
**天气**：{route['weather']} {route['temperature']}
**行程**：{route['schedule']}
**餐饮**：{route['meals']}
**交通**：{route['transportation']}
"""
        
        report += f"""
### 💰 预算估算
| 项目 | 费用 |
|------|------|
| 住宿 | {budget.get('accommodation', '待评估')} |
| 餐饮 | {budget.get('food', '待评估')} |
| 交通 | {budget.get('transportation', '待评估')} |
| 景点门票 | {budget.get('attraction_tickets', '待评估')} |
| **总计** | **{budget.get('total', '待评估')}** |

### ⚠️ 注意事项
"""
        for tip in trip_suggestion.get("tips", []):
            report += f"- {tip}\n"
        
        report += """
---

*本报告由文旅智能体自动生成，数据仅供参考，出行前请查询最新信息。*
"""
        
        return report
    
    def generate_trip_report(self, city: str, days: int, preferences: List[str], data: Dict[str, Any]) -> str:
        """
        生成行程规划报告
        """
        logger.info(f"生成行程规划报告：{city} {days}天")
        
        preferences_text = "、".join(preferences) if preferences else "无特殊偏好"
        
        report = f"""# 🗺️ {city}{days}天行程规划
**旅行偏好**：{preferences_text}
**生成时间**：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 📋 行程概览
"""
        
        for day in data.get("daily_itinerary", []):
            report += f"""
### 📅 第 {day['day']} 天
#### 🌅 上午
- **活动**：{day['morning']['activity']}
- **时长**：{day['morning']['duration']}
- **门票**：{day['morning']['ticket']}

#### 🌞 下午
- **活动**：{day['afternoon']['activity']}
- **时长**：{day['afternoon']['duration']}
- **门票**：{day['afternoon']['ticket']}

#### 🌆 晚上
- **活动**：{day['evening']['activity']}
- **时长**：{day['evening']['duration']}
"""
        
        budget = data.get("budget_breakdown", {})
        report += f"""
---

## 💰 预算估算
| 项目 | 费用 |
|------|------|
| 住宿 | {budget.get('accommodation', '待评估')} |
| 餐饮 | {budget.get('food', '待评估')} |
| 交通 | {budget.get('transportation', '待评估')} |
| 景点门票 | {budget.get('attractions', '待评估')} |
| 其他 | {budget.get('other', '待评估')} |
| **总计** | **{data.get('estimated_total_budget', '待评估')}** |

---

## 💡 旅行小贴士
"""
        for tip in data.get("travel_tips", []):
            report += f"- {tip}\n"
        
        report += """
---

*祝您旅途愉快！*
"""
        
        return report
    
    def generate_weather_report(self, city: str, date: str, data: Dict[str, Any]) -> str:
        """
        生成天气报告
        """
        logger.info(f"生成天气报告：{city} {date}")
        
        date_text = date if date else "今日"
        
        report = f"""# 🌤️ {city} {date_text}天气报告
**生成时间**：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

| 项目 | 详情 |
|------|------|
| 天气 | {data.get('weather', '无数据')} |
| 温度 | {data.get('temperature', '无数据')} |
| 体感温度 | {data.get('feels_like', '无数据')} |
| 湿度 | {data.get('humidity', '无数据')} |
| 风向 | {data.get('wind_direction', '无数据')} |
| 风速 | {data.get('wind_speed', '无数据')} |
| 空气质量 | {data.get('air_quality', '无数据')} |
| AQI指数 | {data.get('aqi', '无数据')} |
| 紫外线指数 | {data.get('uv_index', '无数据')} |
| 降水概率 | {data.get('precipitation_probability', '无数据')} |

---

## 💡 出行建议
{data.get('suggestion', '无建议')}
"""
        
        return report
    
    def generate_attraction_report(self, city: str, category: str, limit: int, data: Dict[str, Any]) -> str:
        """
        生成景点推荐报告
        """
        logger.info(f"生成景点推荐报告：{city} {category} {limit}个")
        
        category_text = category if category else "全部类型"
        
        report = f"""# 🏯 {city} 景点推荐（{category_text}）
**共找到 {data.get('count', 0)} 个相关景点**
**生成时间**：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

| 序号 | 景点名称 | 评分 | 门票价格 | 开放时间 | 推荐指数 |
|------|----------|------|----------|----------|----------|
"""
        
        for i, attr in enumerate(data.get("attractions", []), 1):
            report += f"| {i} | {attr['name']} | ⭐ {attr['rating']} | {attr['ticket_price']} | {attr['opening_hours']} | {attr['recommendation_index']} |\n"
        
        report += """
---

### 📝 景点简介
"""
        
        for i, attr in enumerate(data.get("attractions", []), 1):
            report += f"""
#### {i}. {attr['name']}
{attr['description']}
- 门票：{attr['ticket_price']}
- 开放时间：{attr['opening_hours']}
- 人流量：{attr['crowd_level']}
"""
        
        return report
    
    def generate_comparison_report(self, cities: List[str], data: Dict[str, Any]) -> str:
        """
        生成多城市对比分析报告
        """
        logger.info(f"生成多城市对比报告：{', '.join(cities)}")
        
        cities_text = "、".join(cities)
        
        report = f"""# 📊 {len(cities)}城文旅对比分析报告
**对比城市**：{cities_text}
**生成时间**：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 🎯 综合对比排名
| 排名 | 城市 | 综合得分 | 性价比 | 推荐指数 |
|------|------|----------|--------|----------|
"""
        
        # 综合排名
        ranked_cities = sorted(data.get("cities", []), key=lambda x: x["composite_score"], reverse=True)
        for i, city in enumerate(ranked_cities, 1):
            report += f"| {i} | {city['name']} | {city['composite_score']} | {city['cost_performance']} | {city['recommendation_index']} |\n"
        
        report += """
---

## 🌤️ 天气情况对比
| 城市 | 近期天气 | 平均温度 | 降水概率 | 空气质量 | 出行友好度 |
|------|----------|----------|----------|----------|------------|
"""
        
        for city in data.get("cities", []):
            weather = city.get("weather", {})
            report += f"| {city['name']} | {weather.get('condition', '无数据')} | {weather.get('avg_temperature', '无数据')} | {weather.get('precipitation_probability', '无数据')} | {weather.get('air_quality', '无数据')} | {weather.get('travel_friendliness', '无数据')} |\n"
        
        report += """
---

## 💰 消费指数对比
| 城市 | 住宿均价 | 餐饮人均 | 交通成本 | 景点门票均价 | 日均消费 |
|------|----------|----------|----------|--------------|----------|
"""
        
        for city in data.get("cities", []):
            cost = city.get("cost", {})
            report += f"| {city['name']} | {cost.get('accommodation_avg', '无数据')} | {cost.get('food_avg', '无数据')} | {cost.get('transportation_avg', '无数据')} | {cost.get('attraction_ticket_avg', '无数据')} | {cost.get('daily_cost', '无数据')} |\n"
        
        report += """
---

## 👥 人流量预测
| 城市 | 近期人流量 | 拥挤程度 | 最佳出行时间 | 人流预警 |
|------|------------|----------|--------------|----------|
"""
        
        for city in data.get("cities", []):
            crowd = city.get("crowd", {})
            report += f"| {city['name']} | {crowd.get('recent_level', '无数据')} | {crowd.get('crowd_degree', '无数据')} | {crowd.get('best_time_to_go', '无数据')} | {crowd.get('warning', '无')} |\n"
        
        report += """
---

## 📈 舆情评价对比
| 城市 | 整体评价 | 正面评价占比 | 投诉率 | 游客满意度 |
|------|----------|--------------|--------|------------|
"""
        
        for city in data.get("cities", []):
            sentiment = city.get("sentiment", {})
            report += f"| {city['name']} | {sentiment.get('overall_rating', '无数据')} | {sentiment.get('positive_rate', '无数据')} | {sentiment.get('complaint_rate', '无数据')} | {sentiment.get('tourist_satisfaction', '无数据')} |\n"
        
        report += """
---

## 💡 对比总结与推荐
### ✅ 最优选择
"""
        report += data.get("summary", {}).get("best_choice", "暂无推荐") + "\n"
        
        report += """
### 🌞 适合人群
"""
        report += data.get("summary", {}).get("suitable_for", "暂无说明") + "\n"
        
        report += """
### 📝 出行建议
"""
        for tip in data.get("summary", {}).get("suggestions", []):
            report += f"- {tip}\n"
        
        report += """
---

*本报告由文旅智能体自动生成，综合得分基于天气、消费、人流量、舆情等多维度加权计算，仅供参考。*
"""
        
        return report
    
    def generate_custom_report(self, template: str, data: Dict[str, Any]) -> str:
        """
        生成自定义报告
        """
        logger.info("生成自定义报告")
        
        # 替换模板变量
        from string import Template
        tpl = Template(template)
        
        # 添加通用变量
        context = {
            "generate_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "current_date": datetime.now().strftime("%Y-%m-%d"),
            **data
        }
        
        try:
            return tpl.substitute(context)
        except KeyError as e:
            logger.error(f"模板变量缺失：{e}")
            return f"⚠️ 报告生成失败，缺少变量：{e}"
