#!/usr/bin/env python3
"""
房产中介网站爬虫配置文件
"""

CONFIG = {
    "anjuke": {
        "name": "安居客",
        "url": "https://www.anjuke.com",
        "city_url_pattern": "https://{city}.anjuke.com",
        "selectors": {
            "price": ".property-price",
            "avg_price": ".property-avg-price",
            "area": ".property-area",
            "location": ".property-location",
            "house_type": ".property-type",
            "age": ".property-age",
            "orientation": ".property-orientation",
            "decoration": ".property-decoration",
            "title": ".property-title"
        },
        "data_pattern": r'"price":"([\d\.]+)",.*"avg_price":"([\d\.]+)",.*"area_num":"([\d\.]+)",.*"house_age":"([\d年]+)",.*"orient":"([^"]+)",.*"fitment_name":"([^"]+)",.*"title":"([^"]+)"',
        "anti_crawler_level": "高",
        "anti_crawler_tips": "安居客有较强的反爬虫机制，需要模拟人类行为、使用随机延迟、设置cookie"
    },
    "ke": {
        "name": "贝壳找房",
        "url": "https://www.ke.com",
        "city_url_pattern": "https://{city_prefix}.ke.com",
        "selectors": {
            "price": ".total-price",
            "avg_price": ".unit-price",
            "area": ".area",
            "location": ".location-text",
            "house_type": ".house-type",
            "age": ".building-age",
            "orientation": ".orientation",
            "decoration": ".decoration",
            "title": ".house-title"
        },
        "city_prefixes": {
            "北京": "bj",
            "上海": "sh",
            "广州": "gz",
            "深圳": "sz",
            "杭州": "hz",
            "成都": "cd",
            "南京": "nj",
            "武汉": "wh",
            "天津": "tj",
            "苏州": "su"
        },
        "data_pattern": r'"totalPrice":"([\d\.]+)",.*"unitPrice":"([\d\.]+)",.*"houseArea":"([\d\.]+)",.*"buildYear":"([\d年]+)",.*"orientation":"([^"]+)",.*"decoration":"([^"]+)",.*"title":"([^"]+)"',
        "anti_crawler_level": "较高",
        "anti_crawler_tips": "贝壳找房对爬虫有较强的检测，建议使用代理IP、会话管理、模拟移动设备"
    },
    "lianjia": {
        "name": "链家",
        "url": "https://www.lianjia.com",
        "city_url_pattern": "https://www.lianjia.com/city/{city}/ershoufang",
        "selectors": {
            "price": ".total-price",
            "avg_price": ".unit-price",
            "area": ".area",
            "location": ".area-text",
            "house_type": ".house-type",
            "age": ".building-age",
            "orientation": ".orientation",
            "decoration": ".decoration",
            "title": ".title-text"
        },
        "city_prefixes": {
            "北京": "bj",
            "上海": "sh",
            "广州": "gz",
            "深圳": "sz",
            "杭州": "hz",
            "成都": "cd",
            "南京": "nj",
            "武汉": "wh",
            "天津": "tj",
            "苏州": "su"
        },
        "data_pattern": r'"priceTotal":"([\d\.]+)",.*"priceUnit":"([\d\.]+)",.*"area":"([\d\.]+)",.*"buildingAge":"([\d年]+)",.*"orientation":"([^"]+)",.*"decoration":"([^"]+)",.*"title":"([^"]+)"',
        "anti_crawler_level": "高",
        "anti_crawler_tips": "链家有很强的验证码机制，建议：1) 使用真实Cookie（先手动完成一次验证）；2) 设置Referer和来源页；3) 使用代理IP；4) 限制访问频率"
    },
    "soufun": {
        "name": "搜房网",
        "url": "https://www.soufun.com",
        "city_url_pattern": "https://{city}.soufun.com",
        "selectors": {
            "price": ".price",
            "avg_price": ".unit-price",
            "area": ".area",
            "location": ".location-text",
            "house_type": ".house-type",
            "age": ".building-age",
            "orientation": ".orientation",
            "decoration": ".decoration",
            "title": ".title"
        },
        "data_pattern": r'"price":"([\d\.]+)",.*"unitPrice":"([\d\.]+)",.*"area":"([\d\.]+)",.*"age":"([\d年]+)",.*"orientation":"([^"]+)",.*"decoration":"([^"]+)",.*"title":"([^"]+)"',
        "anti_crawler_level": "中",
        "anti_crawler_tips": "搜房网反爬虫机制相对温和，但仍需注意频率控制"
    }
}

# 用户代理列表
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36"
]

# 代理IP列表（示例）
PROXY_LIST = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080",
]

# 延迟配置
DELAY_CONFIG = {
    "min_delay": 2,      # 最小延迟（秒）
    "max_delay": 5,      # 最大延迟（秒）
    "batch_delay": 30,   # 批次延迟（秒）
    "batch_size": 10    # 批次大小
}

# 验证码处理策略
CAPTCHA_STRATEGY = {
    "manual": True,     # 手动处理验证码
    "api_service": None, # 验证码API服务URL
    "api_key": None     # API密钥
}

# 会话管理配置
SESSION_CONFIG = {
    "save_session": True,
    "session_file": "real_estate_session.json",
    "restore_session": True
}

# 数据保存配置
DATA_CONFIG = {
    "output_format": ["json", "csv", "excel"],
    "save_screensalhots": True,
    "screenshot_dir": "screenshots"
}