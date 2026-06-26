"""
股票名称→代码映射表
A股常见股票名称到交易代码的映射
"""
NAME_TO_CODE = {
    # 你的持仓
    "铜陵有色": "sz000630",
    "云铝股份": "sz000807",
    "神火股份": "sz000933",
    "四川黄金": "sz001337",
    "双鹭药业": "sz002038",
    "长城电工": "sh600192",
    "四川长虹": "sh600839",
    "华友钴业": "sh603799",

    # 蓝筹
    "贵州茅台": "sh600519",
    "宁德时代": "sz300750",
    "比亚迪": "sz002594",
    "招商银行": "sh600036",
    "中国平安": "sh601318",
    "五粮液": "sz000858",
    "美的集团": "sz000333",
    "紫金矿业": "sh601899",
    "伊利股份": "sh600887",
    "中信证券": "sh600030",
    "药明康德": "sh603259",
    "恒瑞医药": "sh600276",
    "迈瑞医疗": "sz300760",
}

CODE_TO_NAME = {v: k for k, v in NAME_TO_CODE.items()}

def get_code(name):
    """通过股票名称获取代码"""
    return NAME_TO_CODE.get(name, "")

def get_name(code):
    """通过代码获取名称"""
    return CODE_TO_NAME.get(code, "")

def get_market(code):
    """判断市场: sh/sz"""
    return "sh" if code.startswith("6") else "sz"

def get_secid(code):
    """获取东方财富格式的secid"""
    market = "1" if code.startswith("6") else "0"
    return f"{market}.{code}"
