"""
旅行eSIM比价助手 - Travel eSIM Compare
对比全球热门目的地的eSIM套餐和WiFi租借方案，帮出境旅客选到最便宜的上网方式。
"""
import json
import os

PROXY_TOKEN = os.environ.get("PROXY_TOKEN", "")

# ========== eSIM套餐数据库 ==========
# 价格单位：美元（各平台统一定价货币）
ESIM_DB = {
    "日本": {
        "region": "亚洲",
        "plans": [
            {"provider": "Airalo", "plan": "日本 5GB/30天", "price": 9.0, "per_gb": 1.80, "data": "5GB", "days": 30, "network": "NTT Docomo/KDDI", "type": "按量"},
            {"provider": "Airalo", "plan": "日本 10GB/30天", "price": 15.0, "per_gb": 1.50, "data": "10GB", "days": 30, "network": "NTT Docomo/KDDI", "type": "按量"},
            {"provider": "Holafly", "plan": "日本 无限流量/5天", "price": 19.0, "per_gb": None, "data": "无限", "days": 5, "network": "NTT Docomo", "type": "无限"},
            {"provider": "Holafly", "plan": "日本 无限流量/10天", "price": 34.0, "per_gb": None, "data": "无限", "days": 10, "network": "NTT Docomo", "type": "无限"},
            {"provider": "Holafly", "plan": "日本 无限流量/15天", "price": 47.0, "per_gb": None, "data": "无限", "days": 15, "network": "NTT Docomo", "type": "无限"},
            {"provider": "eSIM.net", "plan": "日本 3GB/30天", "price": 8.0, "per_gb": 2.67, "data": "3GB", "days": 30, "network": "SoftBank", "type": "按量"},
            {"provider": "eSIM.net", "plan": "日本 20GB/30天", "price": 26.0, "per_gb": 1.30, "data": "20GB", "days": 30, "network": "SoftBank", "type": "按量"},
            {"provider": "MobiMatter", "plan": "日本 10GB/30天", "price": 12.5, "per_gb": 1.25, "data": "10GB", "days": 30, "network": "NTT Docomo", "type": "按量"},
        ],
        "wifi": {"daily_rent": "9-15元/天", "deposit": "500元", "pickup": "机场取还/快递", "speed": "4G不限速", "devices": "5台共享", "note": "多人出行WiFi蛋更划算"},
        "tips": ["日本网速快，eSIM体验好", "Airalo按量套餐性价比最高", "Holafly无限流量适合重度用户", "买eSIM时选NTT Docomo网络覆盖最好"]
    },
    "泰国": {
        "region": "亚洲",
        "plans": [
            {"provider": "Airalo", "plan": "泰国 5GB/30天", "price": 7.0, "per_gb": 1.40, "data": "5GB", "days": 30, "network": "AIS/DTAC", "type": "按量"},
            {"provider": "Airalo", "plan": "泰国 10GB/30天", "price": 12.0, "per_gb": 1.20, "data": "10GB", "days": 30, "network": "AIS/DTAC", "type": "按量"},
            {"provider": "Holafly", "plan": "泰国 无限流量/5天", "price": 15.0, "per_gb": None, "data": "无限", "days": 5, "network": "AIS", "type": "无限"},
            {"provider": "Holafly", "plan": "泰国 无限流量/10天", "price": 27.0, "per_gb": None, "data": "无限", "days": 10, "network": "AIS", "type": "无限"},
            {"provider": "MobiMatter", "plan": "泰国 5GB/30天", "price": 6.0, "per_gb": 1.20, "data": "5GB", "days": 30, "network": "TrueMove", "type": "按量"},
            {"provider": "eSIM.net", "plan": "泰国 5GB/30天", "price": 7.5, "per_gb": 1.50, "data": "5GB", "days": 30, "network": "AIS", "type": "按量"},
        ],
        "wifi": {"daily_rent": "8-12元/天", "deposit": "500元", "pickup": "机场取还/快递", "speed": "4G", "devices": "5台共享", "note": "泰国当地7-11可买实体SIM卡更便宜(约30元/7天无限)"},
        "tips": ["泰国当地买SIM卡最便宜（7-11有售）", "如果飞机到曼谷素万那普机场，到达层有AIS/TrueMove柜台", "eSIM适合不想换卡或落地后立刻要用的场景"]
    },
    "韩国": {
        "region": "亚洲",
        "plans": [
            {"provider": "Airalo", "plan": "韩国 5GB/30天", "price": 8.0, "per_gb": 1.60, "data": "5GB", "days": 30, "network": "SK Telecom/KT", "type": "按量"},
            {"provider": "Airalo", "plan": "韩国 10GB/30天", "price": 14.0, "per_gb": 1.40, "data": "10GB", "days": 30, "network": "SK Telecom/KT", "type": "按量"},
            {"provider": "Holafly", "plan": "韩国 无限流量/5天", "price": 19.0, "per_gb": None, "data": "无限", "days": 5, "network": "SK Telecom", "type": "无限"},
            {"provider": "Holafly", "plan": "韩国 无限流量/10天", "price": 34.0, "per_gb": None, "data": "无限", "days": 10, "network": "SK Telecom", "type": "无限"},
            {"provider": "MobiMatter", "plan": "韩国 10GB/30天", "price": 13.0, "per_gb": 1.30, "data": "10GB", "days": 30, "network": "SK Telecom", "type": "按量"},
        ],
        "wifi": {"daily_rent": "8-12元/天", "deposit": "500元", "pickup": "机场取还/快递", "speed": "4G/5G", "devices": "5台共享", "note": "韩国WiFi蛋支持5G网速更快"},
        "tips": ["韩国网速全球前列，eSIM和WiFi体验都很好", "首尔地铁免费WiFi覆盖广，轻度用户可不买流量", "Airalo的SK Telecom网络覆盖最好"]
    },
    "新加坡": {
        "region": "亚洲",
        "plans": [
            {"provider": "Airalo", "plan": "新加坡 5GB/30天", "price": 7.0, "per_gb": 1.40, "data": "5GB", "days": 30, "network": "Singtel/StarHub", "type": "按量"},
            {"provider": "Holafly", "plan": "新加坡 无限流量/5天", "price": 15.0, "per_gb": None, "data": "无限", "days": 5, "network": "Singtel", "type": "无限"},
            {"provider": "MobiMatter", "plan": "新加坡 5GB/30天", "price": 6.5, "per_gb": 1.30, "data": "5GB", "days": 30, "network": "StarHub", "type": "按量"},
        ],
        "wifi": {"daily_rent": "8-12元/天", "deposit": "500元", "pickup": "机场取还/快递", "speed": "4G", "devices": "5台共享", "note": "新加坡免费WiFi覆盖广(机场/商场/地铁)"},
        "tips": ["新加坡免费WiFi覆盖广，轻度用户可能不需要买流量", "樟宜机场有免费WiFi，落地即可使用"]
    },
    "越南": {
        "region": "亚洲",
        "plans": [
            {"provider": "Airalo", "plan": "越南 5GB/30天", "price": 6.5, "per_gb": 1.30, "data": "5GB", "days": 30, "network": "Viettel", "type": "按量"},
            {"provider": "Holafly", "plan": "越南 无限流量/5天", "price": 15.0, "per_gb": None, "data": "无限", "days": 5, "network": "Viettel", "type": "无限"},
        ],
        "wifi": {"daily_rent": "8-10元/天", "deposit": "500元", "pickup": "快递", "speed": "4G", "devices": "5台共享", "note": "越南当地买SIM卡非常便宜(约15元/7天)"},
        "tips": ["当地买SIM卡最划算，机场就有卖", "Viettel网络覆盖最好，偏远地区也能用"]
    },
    "马来西亚": {
        "region": "亚洲",
        "plans": [
            {"provider": "Airalo", "plan": "马来西亚 5GB/30天", "price": 7.0, "per_gb": 1.40, "data": "5GB", "days": 30, "network": "Maxis/Celcom", "type": "按量"},
            {"provider": "Holafly", "plan": "马来西亚 无限流量/5天", "price": 15.0, "per_gb": None, "data": "无限", "days": 5, "network": "Maxis", "type": "无限"},
        ],
        "wifi": {"daily_rent": "8-12元/天", "deposit": "500元", "pickup": "机场取还/快递", "speed": "4G", "devices": "5台共享", "note": ""},
        "tips": ["吉隆坡机场可买当地SIM卡，价格约20元起"]
    },
    "美国": {
        "region": "北美",
        "plans": [
            {"provider": "Airalo", "plan": "美国 5GB/30天", "price": 12.0, "per_gb": 2.40, "data": "5GB", "days": 30, "network": "T-Mobile/AT&T", "type": "按量"},
            {"provider": "Airalo", "plan": "美国 10GB/30天", "price": 20.0, "per_gb": 2.00, "data": "10GB", "days": 30, "network": "T-Mobile/AT&T", "type": "按量"},
            {"provider": "Airalo", "plan": "美国 20GB/30天", "price": 36.0, "per_gb": 1.80, "data": "20GB", "days": 30, "network": "T-Mobile/AT&T", "type": "按量"},
            {"provider": "Holafly", "plan": "美国 无限流量/5天", "price": 20.0, "per_gb": None, "data": "无限", "days": 5, "network": "T-Mobile", "type": "无限"},
            {"provider": "Holafly", "plan": "美国 无限流量/10天", "price": 34.0, "per_gb": None, "data": "无限", "days": 10, "network": "T-Mobile", "type": "无限"},
            {"provider": "Holafly", "plan": "美国 无限流量/20天", "price": 54.0, "per_gb": None, "data": "无限", "days": 20, "network": "T-Mobile", "type": "无限"},
            {"provider": "MobiMatter", "plan": "美国 10GB/30天", "price": 15.0, "per_gb": 1.50, "data": "10GB", "days": 30, "network": "AT&T", "type": "按量"},
            {"provider": "eSIM.net", "plan": "美国 20GB/30天", "price": 33.0, "per_gb": 1.65, "data": "20GB", "days": 30, "network": "T-Mobile", "type": "按量"},
        ],
        "wifi": {"daily_rent": "15-25元/天", "deposit": "800元", "pickup": "机场取还/快递", "speed": "4G/5G", "devices": "5台共享", "note": "美国WiFi蛋较贵，eSIM更划算"},
        "tips": ["美国T-Mobile覆盖城市好，偏远地区AT&T更强", "Holafly无限流量是长途最佳选择", "MobiMatter的AT&T套餐在农村地区信号更好"]
    },
    "加拿大": {
        "region": "北美",
        "plans": [
            {"provider": "Airalo", "plan": "加拿大 5GB/30天", "price": 12.0, "per_gb": 2.40, "data": "5GB", "days": 30, "network": "Rogers/Bell", "type": "按量"},
            {"provider": "Holafly", "plan": "加拿大 无限流量/5天", "price": 20.0, "per_gb": None, "data": "无限", "days": 5, "network": "Rogers", "type": "无限"},
            {"provider": "MobiMatter", "plan": "加拿大 10GB/30天", "price": 17.0, "per_gb": 1.70, "data": "10GB", "days": 30, "network": "Bell", "type": "按量"},
        ],
        "wifi": {"daily_rent": "15-20元/天", "deposit": "800元", "pickup": "快递", "speed": "4G", "devices": "5台共享", "note": "加拿大偏远地区信号覆盖一般"},
        "tips": ["加拿大偏远地区信号覆盖弱，建议提前下载离线地图", "城市区域eSIM体验好"]
    },
    "英国": {
        "region": "欧洲",
        "plans": [
            {"provider": "Airalo", "plan": "英国 5GB/30天", "price": 8.0, "per_gb": 1.60, "data": "5GB", "days": 30, "network": "EE/Three", "type": "按量"},
            {"provider": "Airalo", "plan": "英国 10GB/30天", "price": 14.0, "per_gb": 1.40, "data": "10GB", "days": 30, "network": "EE/Three", "type": "按量"},
            {"provider": "Holafly", "plan": "英国 无限流量/5天", "price": 15.0, "per_gb": None, "data": "无限", "days": 5, "network": "EE", "type": "无限"},
            {"provider": "Holafly", "plan": "英国 无限流量/10天", "price": 27.0, "per_gb": None, "data": "无限", "days": 10, "network": "EE", "type": "无限"},
            {"provider": "MobiMatter", "plan": "英国 10GB/30天", "price": 13.0, "per_gb": 1.30, "data": "10GB", "days": 30, "network": "Three", "type": "按量"},
        ],
        "wifi": {"daily_rent": "10-15元/天", "deposit": "500元", "pickup": "机场取还/快递", "speed": "4G/5G", "devices": "5台共享", "note": "伦敦免费WiFi覆盖广"},
        "tips": ["英国免费WiFi覆盖广（咖啡厅/商场/地铁）", "如需前往欧洲其他国家，直接买欧洲区域套餐更划算"]
    },
    "法国": {
        "region": "欧洲",
        "plans": [
            {"provider": "Airalo", "plan": "法国 5GB/30天", "price": 8.0, "per_gb": 1.60, "data": "5GB", "days": 30, "network": "Orange/SFR", "type": "按量"},
            {"provider": "Holafly", "plan": "法国 无限流量/5天", "price": 15.0, "per_gb": None, "data": "无限", "days": 5, "network": "Orange", "type": "无限"},
            {"provider": "MobiMatter", "plan": "法国 10GB/30天", "price": 13.0, "per_gb": 1.30, "data": "10GB", "days": 30, "network": "SFR", "type": "按量"},
        ],
        "wifi": {"daily_rent": "10-15元/天", "deposit": "500元", "pickup": "机场取还/快递", "speed": "4G", "devices": "5台共享", "note": "巴黎免费WiFi较多"},
        "tips": ["巴黎咖啡厅和商场多有免费WiFi", "如需去多国直接买欧洲区域套餐"]
    },
    "德国": {
        "region": "欧洲",
        "plans": [
            {"provider": "Airalo", "plan": "德国 5GB/30天", "price": 8.0, "per_gb": 1.60, "data": "5GB", "days": 30, "network": "Telekom/Vodafone", "type": "按量"},
            {"provider": "Holafly", "plan": "德国 无限流量/5天", "price": 15.0, "per_gb": None, "data": "无限", "days": 5, "network": "Telekom", "type": "无限"},
            {"provider": "MobiMatter", "plan": "德国 10GB/30天", "price": 13.0, "per_gb": 1.30, "data": "10GB", "days": 30, "network": "Vodafone", "type": "按量"},
        ],
        "wifi": {"daily_rent": "10-15元/天", "deposit": "500元", "pickup": "快递", "speed": "4G", "devices": "5台共享", "note": ""},
        "tips": ["德国Telekom网络覆盖最好", "免费WiFi不如英国/法国多"]
    },
    "欧洲": {
        "region": "欧洲",
        "plans": [
            {"provider": "Airalo", "plan": "欧洲 5GB/30天", "price": 12.0, "per_gb": 2.40, "data": "5GB", "days": 30, "network": "多国漫游", "type": "按量"},
            {"provider": "Airalo", "plan": "欧洲 10GB/30天", "price": 20.0, "per_gb": 2.00, "data": "10GB", "days": 30, "network": "多国漫游", "type": "按量"},
            {"provider": "Holafly", "plan": "欧洲 无限流量/5天", "price": 27.0, "per_gb": None, "data": "无限", "days": 5, "network": "多国漫游", "type": "无限"},
            {"provider": "Holafly", "plan": "欧洲 无限流量/10天", "price": 44.0, "per_gb": None, "data": "无限", "days": 10, "network": "多国漫游", "type": "无限"},
            {"provider": "Holafly", "plan": "欧洲 无限流量/15天", "price": 59.0, "per_gb": None, "data": "无限", "days": 15, "network": "多国漫游", "type": "无限"},
            {"provider": "MobiMatter", "plan": "欧洲 10GB/30天", "price": 18.0, "per_gb": 1.80, "data": "10GB", "days": 30, "network": "多国漫游", "type": "按量"},
            {"provider": "eSIM.net", "plan": "欧洲 20GB/30天", "price": 35.0, "per_gb": 1.75, "data": "20GB", "days": 30, "network": "多国漫游", "type": "按量"},
        ],
        "wifi": {"daily_rent": "15-20元/天", "deposit": "800元", "pickup": "机场取还/快递", "speed": "4G", "devices": "5台共享", "note": "欧洲区域套餐覆盖30+国家"},
        "tips": ["多国游必选区域套餐，单国套餐跨境会断网", "Holafly欧洲无限套餐是长途多国游最佳选择", "Airalo欧洲套餐覆盖32国，含申根区+英国"]
    },
    "澳大利亚": {
        "region": "大洋洲",
        "plans": [
            {"provider": "Airalo", "plan": "澳洲 5GB/30天", "price": 9.0, "per_gb": 1.80, "data": "5GB", "days": 30, "network": "Optus/Telstra", "type": "按量"},
            {"provider": "Airalo", "plan": "澳洲 10GB/30天", "price": 16.0, "per_gb": 1.60, "data": "10GB", "days": 30, "network": "Optus/Telstra", "type": "按量"},
            {"provider": "Holafly", "plan": "澳洲 无限流量/5天", "price": 19.0, "per_gb": None, "data": "无限", "days": 5, "network": "Optus", "type": "无限"},
            {"provider": "Holafly", "plan": "澳洲 无限流量/10天", "price": 34.0, "per_gb": None, "data": "无限", "days": 10, "network": "Optus", "type": "无限"},
            {"provider": "MobiMatter", "plan": "澳洲 10GB/30天", "price": 14.0, "per_gb": 1.40, "data": "10GB", "days": 30, "network": "Telstra", "type": "按量"},
        ],
        "wifi": {"daily_rent": "12-18元/天", "deposit": "600元", "pickup": "机场取还/快递", "speed": "4G/5G", "devices": "5台共享", "note": "澳洲偏远地区信号差，Telstra覆盖最好"},
        "tips": ["Telstra在偏远地区覆盖最好（如大洋路/乌鲁鲁）", "Optus在城市体验好但偏远地区信号差"]
    },
    "新西兰": {
        "region": "大洋洲",
        "plans": [
            {"provider": "Airalo", "plan": "新西兰 5GB/30天", "price": 9.0, "per_gb": 1.80, "data": "5GB", "days": 30, "network": "Spark/Vodafone", "type": "按量"},
            {"provider": "Holafly", "plan": "新西兰 无限流量/5天", "price": 19.0, "per_gb": None, "data": "无限", "days": 5, "network": "Spark", "type": "无限"},
        ],
        "wifi": {"daily_rent": "12-15元/天", "deposit": "500元", "pickup": "快递", "speed": "4G", "devices": "5台共享", "note": "新西兰南岛偏远地区信号差"},
        "tips": ["新西兰南岛自驾信号覆盖不稳定，建议下载离线地图", "Spark网络覆盖比Vodafone广"]
    },
    "阿联酋": {
        "region": "中东",
        "plans": [
            {"provider": "Airalo", "plan": "阿联酋 5GB/30天", "price": 12.0, "per_gb": 2.40, "data": "5GB", "days": 30, "network": "Etisalat/du", "type": "按量"},
            {"provider": "Holafly", "plan": "阿联酋 无限流量/5天", "price": 19.0, "per_gb": None, "data": "无限", "days": 5, "network": "Etisalat", "type": "无限"},
        ],
        "wifi": {"daily_rent": "15-20元/天", "deposit": "800元", "pickup": "机场取还", "speed": "4G/5G", "devices": "5台共享", "note": "迪拜免费WiFi覆盖广"},
        "tips": ["迪拜商场和机场有大量免费WiFi", "阿联酋eSIM价格偏高，轻度用户靠免费WiFi即可"]
    },
    "土耳其": {
        "region": "中东",
        "plans": [
            {"provider": "Airalo", "plan": "土耳其 5GB/30天", "price": 8.0, "per_gb": 1.60, "data": "5GB", "days": 30, "network": "Turkcell", "type": "按量"},
            {"provider": "Holafly", "plan": "土耳其 无限流量/5天", "price": 15.0, "per_gb": None, "data": "无限", "days": 5, "network": "Turkcell", "type": "无限"},
        ],
        "wifi": {"daily_rent": "10-15元/天", "deposit": "500元", "pickup": "快递", "speed": "4G", "devices": "5台共享", "note": "土耳其当地SIM卡也便宜"},
        "tips": ["伊斯坦布尔机场有Turkcell柜台，当地买SIM卡也很方便"]
    },
    "印度": {
        "region": "亚洲",
        "plans": [
            {"provider": "Airalo", "plan": "印度 5GB/30天", "price": 6.0, "per_gb": 1.20, "data": "5GB", "days": 30, "network": "Airtel/Jio", "type": "按量"},
            {"provider": "Holafly", "plan": "印度 无限流量/5天", "price": 15.0, "per_gb": None, "data": "无限", "days": 5, "network": "Airtel", "type": "无限"},
        ],
        "wifi": {"daily_rent": "8-12元/天", "deposit": "500元", "pickup": "快递", "speed": "4G", "devices": "5台共享", "note": "印度当地SIM卡极便宜(Jio约10元/28天)"},
        "tips": ["印度当地买Jio SIM卡最便宜（约10元/28天无限流量）", "需要护照+照片在机场柜台办理"]
    },
    "印度尼西亚": {
        "region": "亚洲",
        "plans": [
            {"provider": "Airalo", "plan": "印尼 5GB/30天", "price": 7.0, "per_gb": 1.40, "data": "5GB", "days": 30, "network": "Telkomsel", "type": "按量"},
            {"provider": "Holafly", "plan": "印尼 无限流量/5天", "price": 15.0, "per_gb": None, "data": "无限", "days": 5, "network": "Telkomsel", "type": "无限"},
        ],
        "wifi": {"daily_rent": "8-10元/天", "deposit": "500元", "pickup": "快递", "speed": "4G", "devices": "5台共享", "note": "巴厘岛当地SIM卡便宜"},
        "tips": ["巴厘岛机场有Telkomsel柜台，当地买SIM卡更便宜", "巴厘岛偏远地区（乌布山区）信号弱"]
    },
    "菲律宾": {
        "region": "亚洲",
        "plans": [
            {"provider": "Airalo", "plan": "菲律宾 5GB/30天", "price": 7.0, "per_gb": 1.40, "data": "5GB", "days": 30, "network": "Globe/Smart", "type": "按量"},
            {"provider": "Holafly", "plan": "菲律宾 无限流量/5天", "price": 15.0, "per_gb": None, "data": "无限", "days": 5, "network": "Globe", "type": "无限"},
        ],
        "wifi": {"daily_rent": "8-10元/天", "deposit": "500元", "pickup": "快递", "speed": "4G", "devices": "5台共享", "note": "海岛信号不稳定"},
        "tips": ["Globe在城区好，Smart在海岛覆盖更广", "长滩/巴拉望等海岛WiFi信号不稳定，建议eSIM备用"]
    },
    "俄罗斯": {
        "region": "欧洲",
        "plans": [
            {"provider": "Airalo", "plan": "俄罗斯 5GB/30天", "price": 8.0, "per_gb": 1.60, "data": "5GB", "days": 30, "network": "MTS/MegaFon", "type": "按量"},
            {"provider": "MobiMatter", "plan": "俄罗斯 10GB/30天", "price": 15.0, "per_gb": 1.50, "data": "10GB", "days": 30, "network": "MegaFon", "type": "按量"},
        ],
        "wifi": {"daily_rent": "10-15元/天", "deposit": "500元", "pickup": "快递", "speed": "4G", "devices": "5台共享", "note": ""},
        "tips": ["俄罗斯部分eSIM运营商需VPN才能访问Google等网站", "当地买SIM卡需要护照注册"]
    },
    "埃及": {
        "region": "非洲",
        "plans": [
            {"provider": "Airalo", "plan": "埃及 5GB/30天", "price": 9.0, "per_gb": 1.80, "data": "5GB", "days": 30, "network": "Vodafone Egypt", "type": "按量"},
            {"provider": "Holafly", "plan": "埃及 无限流量/5天", "price": 15.0, "per_gb": None, "data": "无限", "days": 5, "network": "Vodafone Egypt", "type": "无限"},
        ],
        "wifi": {"daily_rent": "10-15元/天", "deposit": "500元", "pickup": "快递", "speed": "3G/4G", "devices": "5台共享", "note": "埃及网速较慢"},
        "tips": ["埃及网速整体偏慢，4G覆盖仅限城市", "金字塔区域信号弱，提前下载离线地图"]
    },
    "巴西": {
        "region": "南美",
        "plans": [
            {"provider": "Airalo", "plan": "巴西 5GB/30天", "price": 10.0, "per_gb": 2.00, "data": "5GB", "days": 30, "network": "Claro/Vivo", "type": "按量"},
            {"provider": "Holafly", "plan": "巴西 无限流量/5天", "price": 19.0, "per_gb": None, "data": "无限", "days": 5, "network": "Claro", "type": "无限"},
        ],
        "wifi": {"daily_rent": "12-18元/天", "deposit": "600元", "pickup": "快递", "speed": "4G", "devices": "5台共享", "note": "巴西偏远地区信号差"},
        "tips": ["圣保罗/里约城市区域4G信号好", "亚马逊区域基本无信号，需卫星通讯设备"]
    },
    "墨西哥": {
        "region": "北美",
        "plans": [
            {"provider": "Airalo", "plan": "墨西哥 5GB/30天", "price": 10.0, "per_gb": 2.00, "data": "5GB", "days": 30, "network": "Telcel/AT&T Mexico", "type": "按量"},
            {"provider": "Holafly", "plan": "墨西哥 无限流量/5天", "price": 19.0, "per_gb": None, "data": "无限", "days": 5, "network": "Telcel", "type": "无限"},
        ],
        "wifi": {"daily_rent": "12-15元/天", "deposit": "600元", "pickup": "快递", "speed": "4G", "devices": "5台共享", "note": ""},
        "tips": ["Telcel覆盖最好，AT&T Mexico在城市也不错", "坎昆度假区WiFi覆盖广"]
    },
    "北美洲": {
        "region": "北美",
        "plans": [
            {"provider": "Airalo", "plan": "北美(美加墨) 5GB/30天", "price": 15.0, "per_gb": 3.00, "data": "5GB", "days": 30, "network": "多国漫游", "type": "按量"},
            {"provider": "Holafly", "plan": "北美 无限流量/10天", "price": 44.0, "per_gb": None, "data": "无限", "days": 10, "network": "多国漫游", "type": "无限"},
        ],
        "wifi": {"daily_rent": "15-25元/天", "deposit": "800元", "pickup": "快递", "speed": "4G/5G", "devices": "5台共享", "note": "三国通用"},
        "tips": ["美加墨三国游选北美区域套餐最方便"]
    },
    "东南亚": {
        "region": "亚洲",
        "plans": [
            {"provider": "Airalo", "plan": "东南亚 5GB/30天", "price": 10.0, "per_gb": 2.00, "data": "5GB", "days": 30, "network": "多国漫游", "type": "按量"},
            {"provider": "Holafly", "plan": "东南亚 无限流量/5天", "price": 27.0, "per_gb": None, "data": "无限", "days": 5, "network": "多国漫游", "type": "无限"},
            {"provider": "MobiMatter", "plan": "东南亚 10GB/30天", "price": 17.0, "per_gb": 1.70, "data": "10GB", "days": 30, "network": "多国漫游", "type": "按量"},
        ],
        "wifi": {"daily_rent": "10-15元/天", "deposit": "500元", "pickup": "快递", "speed": "4G", "devices": "5台共享", "note": "东南亚区域套餐覆盖8国"},
        "tips": ["东南亚多国游选区域套餐，比买单国套餐划算", "覆盖泰国/越南/新加坡/马来西亚/印尼/菲律宾/柬埔寨/缅甸"]
    }
}

# ========== 手机eSIM兼容性数据 ==========
ESIM_COMPAT = {
    "苹果": {
        "支持eSIM": ["iPhone XS", "iPhone XS Max", "iPhone XR", "iPhone 11全系列", "iPhone 12全系列", "iPhone 13全系列", "iPhone 14全系列", "iPhone 15全系列", "iPhone 16全系列", "iPhone SE 2(仅美版)", "iPhone SE 3"],
        "不支持eSIM": ["iPhone X及更早", "国行iPhone SE 2(不支持)"],
        "注意": "中国大陆版iPhone 14及以后支持eSIM（港澳版也支持），国行早期部分型号不支持"
    },
    "三星": {
        "支持eSIM": ["Galaxy S20及以后(S系列)", "Galaxy Note20及以后", "Galaxy Z Fold2及以后", "Galaxy Z Flip5及以后", "Galaxy A54/A55(部分市场)"],
        "不支持eSIM": ["Galaxy S10及更早", "Galaxy A系列大部分(低端)"],
        "注意": "三星国行版eSIM支持取决于运营商，需确认"
    },
    "华为": {
        "支持eSIM": ["Mate 60 Pro+(仅天通卫星)", "Pura 70 Ultra(仅天通卫星)"],
        "不支持eSIM": ["绝大多数华为手机不支持eSIM数据功能"],
        "注意": "华为手机基本不支持eSIM出境上网，建议使用WiFi蛋或当地SIM卡"
    },
    "小米": {
        "支持eSIM": ["小米13(仅部分海外版)", "小米14(仅部分海外版)"],
        "不支持eSIM": ["国行版基本不支持eSIM"],
        "注意": "小米国行版不支持eSIM，海外版部分支持"
    },
    "OPPO": {
        "支持eSIM": ["Find X3及以后(仅海外版)"],
        "不支持eSIM": ["国行版不支持"],
        "注意": "OPPO国行不支持eSIM"
    },
    "Google": {
        "支持eSIM": ["Pixel 2及以后全系列"],
        "不支持eSIM": ["Pixel 1"],
        "注意": "Google Pixel全系列eSIM支持最好，国行/海外版均支持"
    }
}

# 流量消耗参考
DATA_USAGE = {
    "social": {"name": "社交聊天", "daily_mb": 300, "desc": "微信/Line/WhatsApp文字+偶尔图片"},
    "video": {"name": "看视频", "daily_mb": 3000, "desc": "抖音/B站/YouTube 1-2小时"},
    "work": {"name": "办公", "daily_mb": 500, "desc": "邮件/文档/视频会议30分钟"},
    "nav": {"name": "导航地图", "daily_mb": 100, "desc": "Google Maps/高德离线后仅定位"}
}


def esim_search(destination: str, data_gb: str = "", days: str = "") -> str:
    """搜索eSIM套餐"""
    dest = destination.strip()
    result = None

    for key, val in ESIM_DB.items():
        if dest in key or key in dest:
            result = val
            break

    if not result:
        available = list(ESIM_DB.keys())
        return json.dumps({
            "found": False,
            "message": f"暂未收录'{dest}'的eSIM数据。目前收录{len(available)}个目的地：{', '.join(available)}。"
        }, ensure_ascii=False)

    plans = result["plans"]

    # Filter by data/days if specified
    if data_gb:
        try:
            target_gb = float(data_gb)
            plans = [p for p in plans if p["type"] == "无限" or (p.get("per_gb") and float(p["data"].replace("GB", "")) >= target_gb * 0.5)]
        except (ValueError, AttributeError):
            pass

    if days:
        try:
            target_days = int(days)
            plans = [p for p in plans if p["days"] >= target_days]
        except (ValueError, TypeError):
            pass

    # Sort by price
    plans_sorted = sorted(plans, key=lambda p: p["price"])

    # Add ranking
    for i, p in enumerate(plans_sorted):
        p["rank"] = i + 1

    output = {
        "found": True,
        "destination": dest,
        "region": result.get("region", ""),
        "plans": plans_sorted,
        "recommendation": _get_recommendation(result, data_gb, days)
    }

    return json.dumps(output, ensure_ascii=False)


def _get_recommendation(data, data_gb="", days=""):
    """Generate recommendation based on trip profile"""
    tips = data.get("tips", [])
    rec = []

    if days:
        try:
            d = int(days)
            if d <= 5:
                rec.append("短途旅行推荐Holafly无限流量套餐，不用担心流量不够")
            elif d <= 10:
                rec.append("中等时长推荐Airalo 10GB套餐，性价比最高")
            else:
                rec.append("长途旅行推荐大流量套餐或Holafly无限流量")
        except ValueError:
            pass

    if data_gb:
        try:
            gb = float(data_gb)
            if gb <= 3:
                rec.append("轻度使用选3-5GB套餐即可，Airalo最便宜")
            elif gb <= 10:
                rec.append("中度使用选10GB套餐，MobiMatter和Airalo性价比高")
            else:
                rec.append("重度使用选20GB+或无限流量套餐")
        except ValueError:
            pass

    rec.extend(tips[:3])
    return rec


def wifi_rental(destination: str, pickup: str = "") -> str:
    """查询WiFi租借方案"""
    dest = destination.strip()
    result = None

    for key, val in ESIM_DB.items():
        if dest in key or key in dest:
            result = val
            break

    if not result:
        return json.dumps({
            "found": False,
            "message": f"暂未收录'{dest}'的WiFi租借信息。"
        }, ensure_ascii=False)

    wifi = result.get("wifi", {})

    # Domestic WiFi rental platforms
    platforms = [
        {"name": "漫游超人", "coverage": "全球200+国家", "feature": "5G机型可选，支持机场取还", "payment": "支付宝/微信"},
        {"name": "环球漫游", "coverage": "全球150+国家", "feature": "老牌平台，信号稳定", "payment": "支付宝/微信"},
        {"name": "游伴伴", "coverage": "全球100+国家", "feature": "价格实惠，快递方便", "payment": "支付宝/微信"},
    ]

    output = {
        "found": True,
        "destination": dest,
        "wifi_egg": wifi,
        "platforms": platforms,
        "vs_esim": _compare_wifi_esim(result, pickup),
    }

    return json.dumps(output, ensure_ascii=False)


def _compare_wifi_esim(data, pickup=""):
    """Compare WiFi vs eSIM recommendation"""
    plans = data.get("plans", [])
    cheapest = min(plans, key=lambda p: p["price"]) if plans else None

    return {
        "1人出行": "eSIM更划算，单人多日约$8-15",
        "2人出行": "eSIM各买一张，总价可能比WiFi蛋略高但更灵活",
        "3-5人出行": "WiFi蛋更划算，5人共享一台，日均10-20元",
        "结论": "1-2人选eSIM，3人以上选WiFi蛋。手机不支持eSIM的选WiFi蛋。"
    }


def data_tips(destination: str, usage: str = "social") -> str:
    """出境上网省钱技巧"""
    dest = destination.strip()
    result = None

    for key, val in ESIM_DB.items():
        if dest in key or key in dest:
            result = val
            break

    usage_map = {
        "social": "social", "聊天": "social", "社交": "social",
        "video": "video", "视频": "video", "追剧": "video",
        "work": "work", "办公": "work", "出差": "work",
        "nav": "nav", "导航": "nav", "地图": "nav",
    }
    mapped_usage = usage_map.get(usage.lower(), "social")
    usage_info = DATA_USAGE.get(mapped_usage, DATA_USAGE["social"])

    tips = {
        "destination": dest,
        "usage_type": usage_info["name"],
        "daily_estimate": f"{usage_info['daily_mb']}MB/天",
        "usage_desc": usage_info["desc"],
        "7day_estimate": f"{usage_info['daily_mb'] * 7 / 1000:.1f}GB/7天",
        "14day_estimate": f"{usage_info['daily_mb'] * 14 / 1000:.1f}GB/14天",
        "phone_compat": ESIM_COMPAT,
        "general_tips": [
            "出发前下载离线地图（Google Maps/高德），可省80%导航流量",
            "酒店和咖啡厅的WiFi用于看视频/更新APP，eSIM流量用于导航和即时通讯",
            "关闭手机后台APP自动刷新和云同步（照片/iCloud），避免偷跑流量",
            "国内手机号开通国际漫游（仅接短信验证码），数据流量用eSIM",
            "WhatsApp/Line通话比手机漫游便宜很多，有WiFi时优先用网络通话",
        ],
    }

    if result:
        tips["local_tips"] = result.get("tips", [])
        tips["wifi_info"] = result.get("wifi", {})

    return json.dumps(tips, ensure_ascii=False)


# ========== Tool Registry ==========
TOOLS = {
    "esim_search": {"fn": esim_search, "desc": "搜索eSIM套餐"},
    "wifi_rental": {"fn": wifi_rental, "desc": "查询WiFi租借方案"},
    "data_tips": {"fn": data_tips, "desc": "出境上网省钱技巧"},
}


def run(tool_name: str, **kwargs):
    """Execute a tool by name."""
    tool = TOOLS.get(tool_name)
    if not tool:
        return json.dumps({"error": f"Unknown tool: {tool_name}"}, ensure_ascii=False)
    try:
        return tool["fn"](**kwargs)
    except TypeError as e:
        return json.dumps({"error": f"参数错误: {str(e)}"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": f"执行错误: {str(e)}"}, ensure_ascii=False)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python main.py <tool_name> [args...]")
        sys.exit(1)

    tool = sys.argv[1]
    args = {}
    i = 2
    while i < len(sys.argv) - 1:
        key = sys.argv[i].lstrip("-")
        args[key] = sys.argv[i + 1]
        i += 2

    print(run(tool, **args))
