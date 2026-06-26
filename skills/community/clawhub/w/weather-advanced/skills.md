from skills.base import BaseSkill
import requests
from typing import Dict, Any

class WeatherAdvancedSkill(BaseSkill):
    # 技能唯一标识，和基础版区分，平台不冲突
    name = "weather_advanced_query"
    
    # 大模型触发专用描述，精准匹配用户意图，自动调用率高
    description = "专业级全国城市天气查询，包含实时天气、未来7天预报、空气质量、生活指数、紫外线、穿衣建议、感冒风险等全维度信息"

    def execute(self, params: Dict[str, Any]) -> str:
        """技能执行入口，标配参数校验和异常捕获"""
        # 校验必填参数
        city = params.get("city", "").strip()
        if not city:
            return "🙋‍♂️ 请告诉我需要查询的城市名称，比如北京、杭州、成都哦～"

        try:
            # 调用优化版稳定接口，超时短、容错强
            weather_data = self._get_advanced_weather(city)
            return self._format_advanced_result(city, weather_data)

        except requests.exceptions.Timeout:
            return "⏱️ 天气查询超时，请稍后再试，可更换城市名称重试"
        except requests.exceptions.ConnectionError:
            return "🔌 网络连接异常，请检查网络后重新查询"
        except ValueError as ve:
            return f"❌ {str(ve)}"
        except Exception as e:
            return f"⚠️ 查询失败：暂不支持该城市或接口临时维护，错误信息：{str(e)}"

    def _get_advanced_weather(self, city: str) -> Dict[str, Any]:
        """
        升级版专用接口：免费无Key、国内高速、数据全面
        支持实时天气+7天预报+空气质量+生活指数，适配国内所有地级市
        """
        url = "https://api.vvhan.com/api/weather"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        params = {"city": city, "type": "all"}
        
        resp = requests.get(url, params=params, headers=headers, timeout=12)
        # 强制校验接口响应状态
        resp.raise_for_status()
        data = resp.json()

        if not data.get("success", False):
            raise ValueError("城市名称输入有误或暂不支持该地区，请更换标准城市名重试")
        
        return data.get("data", {})

    def _format_advanced_result(self, city: str, data: Dict[str, Any]) -> str:
        """
        高颜值格式化输出，分层清晰，信息完整，适配大模型返回
        包含基础天气、7天预报、空气质量、生活指数四大模块
        """
        # 基础实时天气数据
        city_name = data.get("city", city)
        current_date = data.get("date", "未知日期")
        current_week = data.get("week", "未知星期")
        weather_type = data.get("type", "暂无数据")
        temp_low = data.get("low", "暂无")
        temp_high = data.get("high", "暂无")
        wind_direct = data.get("fengxiang", "暂无")
        wind_power = data.get("fengli", "暂无")
        humidity = data.get("humidity", "暂无")
        air_quality = data.get("air", "暂无数据")
        uv_index = data.get("uv", "暂无")
        tip = data.get("tip", "暂无建议")

        # 未来7天预报数据处理
        forecast_list = data.get("forecast", [])
        forecast_text = ""
        if forecast_list:
            forecast_text = "\n".join([
                f"📅 {day.get('date', '')} {day.get('week', '')} | {day.get('type', '晴')} | {day.get('low', '')}~{day.get('high', '')}"
                for day in forecast_list
            ])
        else:
            forecast_text = "暂无未来7天预报数据"

        # 生活指数模块，新增实用信息
        life_tips = (
            f"😷 空气质量：{air_quality}\n"
            f"☀️ 紫外线强度：{uv_index}\n"
            f"🧥 穿衣建议：{tip}\n"
            f"💨 风力详情：{wind_direct} {wind_power}"
        )

        # 最终拼接结果，分段清晰，符号美观，用户易读
        result = (
            f"🌤【{city_name}】专业版天气预报\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📅 当前日期：{current_date} {current_week}\n"
            f"☁️ 实时天气：{weather_type}\n"
            f"🌡 温度区间：{temp_low} ~ {temp_high}\n"
            f"💧 空气湿度：{humidity}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📆 未来7天预报：\n"
            f"{forecast_text}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 生活实用指数：\n"
            f"{life_tips}"
        )
        return result
