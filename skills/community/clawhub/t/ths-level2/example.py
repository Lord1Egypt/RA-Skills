"""
同花顺Level2数据获取 - 完整示例

演示如何使用各种方法获取同花顺Level2数据
"""

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from ths_client import THSClient, THSLocalReader
from ths_memory_reader import THSMemoryReader


def demo_local_reader():
    """演示本地数据读取"""
    print("\n" + "=" * 60)
    print("方法1: 读取本地SQLite数据库")
    print("=" * 60)
    
    reader = THSLocalReader(r"D:\同花顺远航版")
    
    # 获取所有股票
    all_stocks = reader.get_all_stocks()
    print(f"\n数据库中共有 {len(all_stocks)} 只股票")
    
    # 显示前10只
    print("\n前10只股票:")
    for stock in all_stocks[:10]:
        print(f"  {stock['code']} - {stock['name']} ({stock['market']})")
    
    # 搜索股票
    print("\n搜索'平安':")
    results = reader.search_stock("平安")
    for stock in results[:5]:
        print(f"  {stock['code']} - {stock['name']}")
    
    # 搜索'茅台'
    print("\n搜索'茅台':")
    results = reader.search_stock("茅台")
    for stock in results[:5]:
        print(f"  {stock['code']} - {stock['name']}")


def demo_tcp_client():
    """演示TCP客户端连接"""
    print("\n" + "=" * 60)
    print("方法2: TCP直接连接服务器")
    print("=" * 60)
    
    print("\n注意: 此方法需要分析完整的TCP协议")
    print("建议使用Wireshark抓包分析数据格式")
    
    client = THSClient(r"D:\同花顺远航版")
    
    if client.connect():
        print("\n连接成功!")
        print("服务器信息已获取")
        
        # 显示服务器列表
        print("\n已知服务器列表:")
        for host, port in THSClient.SERVERS:
            print(f"  {host}:{port}")
        
        client.close()
    else:
        print("\n连接失败")
        print("可能原因:")
        print("  1. 网络不通")
        print("  2. 需要登录认证")
        print("  3. 服务器地址已更新")


def demo_memory_reader():
    """演示内存读取"""
    print("\n" + "=" * 60)
    print("方法3: 读取进程内存")
    print("=" * 60)
    
    print("\n注意: 此方法需要管理员权限")
    print("需要同花顺客户端正在运行")
    
    reader = THSMemoryReader()
    
    if reader.connect():
        print("\n成功连接到同花顺进程!")
        print(f"进程ID: {reader.process_id}")
        
        # 尝试查找股票数据
        print("\n搜索股票 '600000' 在内存中的位置...")
        addr = reader.find_stock_data('600000')
        if addr:
            print(f"  找到地址: 0x{addr:X}")
        
        reader.disconnect()
    else:
        print("\n连接失败，请确保:")
        print("  1. 同花顺正在运行")
        print("  2. 以管理员权限运行此脚本")


def demo_protocol_info():
    """显示协议信息"""
    print("\n" + "=" * 60)
    print("Level2 数据协议摘要")
    print("=" * 60)
    
    from ths_protocol_generated import THSProtocol
    
    print("\n生成示例请求:")
    
    # 成交明细
    print("\n1. 成交明细 (Level2 Tick数据):")
    req = THSProtocol.build_request(205, market='USZA', code='000001', start=-50, end=0, datatype=[1, 12, 49, 10, 18])
    print(f"   {req}")
    
    # 集合竞价
    print("\n2. 集合竞价数据:")
    import time
    now = int(time.time())
    req = THSProtocol.build_request(204, market='USZA', code='000001', start=now-3600, end=now, datatype=[10, 49, 19, 27, 33])
    print(f"   {req}")
    
    # 分时数据
    print("\n3. 分时数据:")
    req = THSProtocol.build_request(207, market='USZA', code='000001', date=0, datatype=[13, 19, 10, 1])
    print(f"   {req}")
    
    # K线数据
    print("\n4. 日K线数据:")
    req = THSProtocol.build_request(210, market='USZA', code='000001', start=-100, end=0, datatype=[1, 7, 8, 9, 11, 13, 19], period=16384, fuquan='Q')
    print(f"   {req}")
    
    # 十档行情
    print("\n5. 十档行情 (Level2深度):")
    req = THSProtocol.build_request(202, market='USZA', codelist='000001', datatype=[27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50])
    print(f"   {req}")


def main():
    """主函数"""
    print("=" * 60)
    print("同花顺Level2数据获取 - 完整示例")
    print("=" * 60)
    
    # 1. 本地数据读取 (最简单，一定能工作)
    demo_local_reader()
    
    # 2. 显示协议信息
    demo_protocol_info()
    
    # 3. TCP连接 (需要进一步协议分析)
    # demo_tcp_client()
    
    # 4. 内存读取 (需要管理员权限)
    # demo_memory_reader()
    
    print("\n" + "=" * 60)
    print("下一步建议:")
    print("=" * 60)
    print("""
1. 使用Wireshark抓包分析TCP协议
   - 过滤条件: tcp.port == 9601 or tcp.port == 8602
   - 分析数据包格式和登录流程

2. 使用x64dbg分析内存结构
   - 搜索股票代码定位数据结构
   - 分析字段偏移量

3. 研究SDK DLL
   - 使用IDA Pro分析 Hevo.Sdk.dll
   - 查找导出函数和调用方式

4. 官方API (如果有)
   - 同花顺可能提供付费API服务
   - 咨询官方客服获取Level2数据API
""")


if __name__ == "__main__":
    main()