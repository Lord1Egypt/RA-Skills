#!/usr/bin/env python3
"""
TDX股票查询技能测试脚本
测试所有API接口功能
"""

from main import TDXStockQuery, format_price, format_volume
import json


def print_test_result(test_name: str, result: dict):
    """打印测试结果"""
    print(f"\n{'='*60}")
    print(f"测试: {test_name}")
    print(f"{'='*60}")
    
    if result.get('code') == 0:
        print(f"✅ 成功: {result.get('message', 'success')}")
        if 'data' in result:
            data = result['data']
            if isinstance(data, (dict, list)):
                print(f"数据: {json.dumps(data, ensure_ascii=False, indent=2)[:500]}...")
            else:
                print(f"数据: {data}")
    else:
        print(f"❌ 失败: {result.get('message', 'unknown error')}")


def main():
    print("="*60)
    print("TDX股票查询技能 - 完整API测试")
    print("="*60)
    
    try:
        stock_query = TDXStockQuery()
        print(f"\n✅ 成功连接到API: {stock_query.api_url}")
    except ValueError as e:
        print(f"\n❌ 初始化失败: {e}")
        return
    except Exception as e:
        print(f"\n❌ 连接失败: {e}")
        return
    
    test_count = 0
    success_count = 0
    
    # 1. 健康检查
    test_count += 1
    result = stock_query.health_check()
    print_test_result("1. 健康检查", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 2. 服务状态
    test_count += 1
    result = stock_query.get_server_status()
    print_test_result("2. 服务状态", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 3. 搜索股票
    test_count += 1
    result = stock_query.search_stock('平安')
    print_test_result("3. 搜索股票（平安）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 4. 获取五档行情
    test_count += 1
    result = stock_query.get_quote(['000001'])
    print_test_result("4. 获取五档行情（000001）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 5. 获取K线数据
    test_count += 1
    result = stock_query.get_kline('000001', 'day')
    print_test_result("5. 获取K线数据（000001, day）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 6. 获取分时数据
    test_count += 1
    result = stock_query.get_minute('000001')
    print_test_result("6. 获取分时数据（000001）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 7. 获取分时成交
    test_count += 1
    result = stock_query.get_trade('000001')
    print_test_result("7. 获取分时成交（000001）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 8. 获取股票综合信息
    test_count += 1
    result = stock_query.get_stock_info('000001')
    print_test_result("8. 获取股票综合信息（000001）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 9. 获取股票代码列表
    test_count += 1
    result = stock_query.get_codes('sh')
    print_test_result("9. 获取股票代码列表（sh）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 10. 批量获取行情
    test_count += 1
    result = stock_query.batch_quote(['000001', '600519'])
    print_test_result("10. 批量获取行情（000001, 600519）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 11. 获取历史K线
    test_count += 1
    result = stock_query.get_kline_history('000001', 'day', limit=10)
    print_test_result("11. 获取历史K线（000001, day, limit=10）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 12. 获取指数数据
    test_count += 1
    result = stock_query.get_index('sh000001', 'day')
    print_test_result("12. 获取指数数据（sh000001, day）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 13. 获取ETF列表
    test_count += 1
    result = stock_query.get_etf('sh', limit=5)
    print_test_result("13. 获取ETF列表（sh, limit=5）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 14. 查询交易日信息
    test_count += 1
    result = stock_query.get_workday()
    print_test_result("14. 查询交易日信息", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 15. 获取市场证券数量
    test_count += 1
    result = stock_query.get_market_count()
    print_test_result("15. 获取市场证券数量", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 16. 获取股票代码列表
    test_count += 1
    result = stock_query.get_stock_codes(limit=10)
    print_test_result("16. 获取股票代码列表（limit=10）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 17. 获取ETF代码列表
    test_count += 1
    result = stock_query.get_etf_codes(limit=10)
    print_test_result("17. 获取ETF代码列表（limit=10）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 18. 获取股票全部历史K线
    test_count += 1
    result = stock_query.get_kline_all('000001', 'day', limit=5)
    print_test_result("18. 获取股票全部历史K线（000001, day, limit=5）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 19. 获取指数全部历史K线
    test_count += 1
    result = stock_query.get_index_all('sh000001', 'day', limit=5)
    print_test_result("19. 获取指数全部历史K线（sh000001, day, limit=5）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 20. 获取交易日范围
    test_count += 1
    result = stock_query.get_workday_range('20241101', '20241130')
    print_test_result("20. 获取交易日范围（20241101-20241130）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 21. 获取历史分时成交（分页）
    test_count += 1
    result = stock_query.get_trade_history('000001', '20241108', count=100)
    print_test_result("21. 获取历史分时成交（000001, 20241108, count=100）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 22. 获取全天分时成交
    test_count += 1
    result = stock_query.get_minute_trade_all('000001')
    print_test_result("22. 获取全天分时成交（000001）", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 23. 查询任务列表
    test_count += 1
    result = stock_query.get_tasks()
    print_test_result("23. 查询任务列表", result)
    if result.get('code') == 0:
        success_count += 1
    
    # 24. 测试价格转换函数
    test_count += 1
    try:
        price_yuan = format_price(12350)
        print(f"\n{'='*60}")
        print(f"测试: 24. 价格转换函数")
        print(f"{'='*60}")
        print(f"✅ 成功: 12350厘 = {price_yuan}元")
        success_count += 1
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"测试: 24. 价格转换函数")
        print(f"{'='*60}")
        print(f"❌ 失败: {e}")
    
    # 25. 测试成交量转换函数
    test_count += 1
    try:
        volume_shares = format_volume(1000)
        print(f"\n{'='*60}")
        print(f"测试: 25. 成交量转换函数")
        print(f"{'='*60}")
        print(f"✅ 成功: 1000手 = {volume_shares}股")
        success_count += 1
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"测试: 25. 成交量转换函数")
        print(f"{'='*60}")
        print(f"❌ 失败: {e}")
    
    # 26. 测试个股新闻查询
    test_count += 1
    try:
        result = stock_query.get_stock_news('603777')
        print(f"\n{'='*60}")
        print(f"测试: 26. 个股新闻查询（603777）")
        print(f"{'='*60}")
        if result.get('code') == 0:
            print(f"✅ 成功: 找到 {len(result.get('data', []))} 条新闻")
            if result.get('data'):
                print(f"第一条新闻: {result['data'][0]['新闻标题']}")
            success_count += 1
        else:
            print(f"⚠️  提示: {result.get('message')}")
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"测试: 26. 个股新闻查询（603777）")
        print(f"{'='*60}")
        print(f"❌ 失败: {e}")
    
    # 27. 测试关键词新闻查询
    test_count += 1
    try:
        result = stock_query.get_stock_news('宁德时代')
        print(f"\n{'='*60}")
        print(f"测试: 27. 关键词新闻查询（宁德时代）")
        print(f"{'='*60}")
        if result.get('code') == 0:
            print(f"✅ 成功: 找到 {len(result.get('data', []))} 条新闻")
            if result.get('data'):
                print(f"第一条新闻: {result['data'][0]['新闻标题']}")
            success_count += 1
        else:
            print(f"⚠️  提示: {result.get('message')}")
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"测试: 27. 关键词新闻查询（宁德时代）")
        print(f"{'='*60}")
        print(f"❌ 失败: {e}")
    
    # 测试总结
    print(f"\n{'='*60}")
    print("测试总结")
    print(f"{'='*60}")
    print(f"总测试数: {test_count}")
    print(f"成功数: {success_count}")
    print(f"失败数: {test_count - success_count}")
    print(f"成功率: {success_count/test_count*100:.1f}%")
    print(f"{'='*60}")
    
    if success_count == test_count:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️  有 {test_count - success_count} 个测试失败")


if __name__ == "__main__":
    main()