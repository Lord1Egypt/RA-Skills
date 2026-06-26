import os
from main import TDXStockQuery

# 设置环境变量
os.environ['TDX_API_URL'] = 'http://10.0.0.8:53270'
os.environ['AKSHARE_API_URL'] = 'http://10.0.0.8:8798'

# 初始化股票查询对象
stock_query = TDXStockQuery()

# 测试股票公告查询功能
try:
    # 测试基本查询
    print("测试1: 基本公告查询")
    result = stock_query.get_stock_disclosure('300058', '20250101', '20250331')
    print(f"结果: {result}")
    print()
    
    # 测试带分类的查询
    print("测试2: 带分类的公告查询")
    result = stock_query.get_stock_disclosure('300058', '20250101', '20251231', category='董事会')
    print(f"结果: {result}")
    print()
    
    # 测试带关键词的查询
    print("测试3: 带关键词的公告查询")
    result = stock_query.get_stock_disclosure('300058', '20250101', '20251231', keyword='担保')
    print(f"结果: {result}")
    print()
    
    print("测试完成!")
except Exception as e:
    print(f"测试过程中发生错误: {str(e)}")
