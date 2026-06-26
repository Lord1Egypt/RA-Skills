# 股票盯盯用户配置文件示例

# 请将此文件复制到 scripts/config.py，并修改 WATCHLIST 配置

WATCHLIST = [
    # 示例配置1：上证A股
    {
        "code": "600362",           # 股票代码：江西铜业
        "name": "江西铜业",         # 股票名称
        "market": "sh",             # 市场：上证 (sh = 上海，sz = 深圳)
        "type": "individual",       # 类型：个股
        "cost": 57.00,              # 持仓成本（元）
        "focus": True,              # 重点关注
        "alerts": {
            "cost_pct_above": 15.0,   # 盈利15%提醒
            "cost_pct_below": -12.0,  # 亏损12%止损
            "change_pct_above": 4.0,  # 日内大涨4%预警
            "change_pct_below": -4.0, # 日内大跌4%预警
            "volume_surge": 2.0       # 放量2倍预警
        }
    },
    
    # 示例配置2：深证A股
    {
        "code": "300383",           # 股票代码：光环新网
        "name": "光环新网",         # 股票名称
        "market": "sz",             # 市场：深证
        "type": "individual",       # 类型：个股
        "cost": 17.00,              # 持仓成本（元）
        "focus": True,              # 重点关注
        "alerts": {
            "cost_pct_above": 15.0,   # 盈利15%提醒
            "cost_pct_below": -12.0,  # 亏损12%止损
            "change_pct_above": 4.0,  # 日内大涨4%预警
            "change_pct_below": -4.0, # 日内大跌4%预警
            "volume_surge": 3.0       # 放量3倍预警
        }
    },
    
    # 示例配置3：ETF基金
    {
        "code": "159892",           # ETF代码：恒生医疗ETF
        "name2": "恒生医疗",         # ETF名称
        "market": "sz",             # 市场：深证
        "type": "etf",              # 类型：ETF基金
        "cost": 0.80,               # 持仓成本（元）
        "focus": True,              # 重点关注
        "alerts": {
            "cost_pct_above": 20.0,   # 盈利20%提醒（ETF波动小）
            "cost_pct_below": -15.0,  # 亏损15%止损
            "change_pct_above": 2.0,  # 日内大涨2%预警（ETF阈值更低）
            "change_pct_below": -2.0,  # 日内大跌2%预警
            "volume_surge": 1.8       # 放量1.8倍预警
        }
    },
    
    # 示例配置4：国际黄金
    {
        "code": "hf_XAU",           # 黄金代码：伦敦金
        "name": "伦敦金",           # 产品名称
        "market": "fx",             # 市场：外汇/贵金属
        "type": "gold",             # 类型：黄金
        "cost": 4800,              # 持仓成本（元/克）
        "focus": True,              # 重点关注
        "alerts": {
            "cost_pct_above": 25.0,   # 盈利25%提醒（黄金波动大）
            "cost_pct_below": -20.0,  # 亏损20%止损
            "change_pct_above": 3.0,  # 日内大涨3%预警
            "change_pct_below": -3.0,  # 日内大跌3%预警
            # 黄金没有成交量预警
        }
    }
]

# 飞书推送配置
FEISHU_TARGET = "ou_78f9e41a60baa905e5c2fe8178216ee6"  # 替换为你的飞书用户 ID

# 智能频率配置（用户可根据需要调整）
SMART_SCHEDULE = {
    "market_open": {"hours": [(9, 30), (11, 30), (13, 0), (15, 0)], "interval": 300},  # 交易时间: 5分钟
    "after_hours": {"interval": 1800},  # 收盘后: 30分钟
    "night": {"hours": [(0, 0), (8, 0)], "interval": 3600},  # 凌晨: 1小时(仅伦敦金)
}

# 安装步骤：
# 1. 复制此文件到 scripts/config.py
# 2. 修改 WATCHLIST 中的股票代码、成本和预警阈值
# 3. 修改 FEISHU_TARGET 为你的飞书用户 ID
# 4. 如果需要，调整 SMART_SCHEDULE 监控频率
# 5. 运行 python3 monitor.py 开始监控