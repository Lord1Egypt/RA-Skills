import tushare as ts

def run(inputs):
    """
    Tushare 股票数据源技能
    """
    # 你的 Tushare Token
    ts.set_token("885cd28a17a52b35e5da6abb8ac11e20e85483affa4c4de8a9e6a928")
    pro = ts.pro_api()

    # 从输入获取参数
    ts_code = inputs.get("ts_code", "")
    limit = inputs.get("limit", 1)

    # 查询股票数据
    data = pro.stock_basic(ts_code=ts_code, limit=limit)
    stock_list = data.to_dict("records")

    return {
        "status": "success",
        "count": len(stock_list),
        "data": stock_list
    }