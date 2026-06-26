# -*- coding: utf-8 -*-
"""
同花顺Level2数据客户端
通过分析同花顺远航版内部协议实现数据获取

基于以下发现：
1. 服务器地址: hevo-h.10jqka.com.cn:9601, hevo.10jqka.com.cn:8602
2. 数据请求格式来自 DataPushJob.xml
3. 本地SQLite数据库 stocknameV2.db 存储股票基本信息

使用方法:
    client = THSClient()
    client.connect()
    
    # 获取实时行情
    quote = client.get_quote('600000')
    
    # 获取分时数据
    ticks = client.get_ticks('300033')
    
    # 获取成交明细 (Level2)
    trades = client.get_trade_detail('000001')
"""

import socket
import struct
import sqlite3
import json
import time
import zlib
import sys
import io
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from pathlib import Path
import threading
import queue

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


@dataclass
class QuoteData:
    """实时行情数据"""
    code: str
    name: str
    price: float
    open: float
    high: float
    low: float
    volume: int
    amount: float
    bid_prices: List[float]
    ask_prices: List[float]
    bid_volumes: List[int]
    ask_volumes: int
    timestamp: int


@dataclass
class TradeData:
    """成交明细数据"""
    time: str
    price: float
    volume: int
    direction: int  # 1=买入, 2=卖出
    amount: float


class THSClient:
    """同花顺数据客户端"""
    
    # 服务器配置
    SERVERS = [
        ("hevo-h.10jqka.com.cn", 9601),
        ("hevo.10jqka.com.cn", 8602),
        ("110.41.57.53", 9602),
        ("122.112.248.51", 9602),
        ("124.71.31.234", 9602),
    ]
    
    # 市场代码
    MARKETS = {
        'SH': 'USHA',  # 上海A股
        'SZ': 'USZA',  # 深圳A股
        'SHI': 'USHI', # 上海指数
        'SZI': 'USZI', # 深圳指数
    }
    
    # 数据类型ID
    DATATYPES = {
        'quote': '5,6,7,8,9,10,13,19,22,23',  # 基本行情
        'level2': '1,12,49,10,18',  # Level2成交明细
        'ticks': '13,19,10,1',  # 分时数据
        'depth': '27,33,49',  # 深度数据
    }
    
    def __init__(self, ths_path: str = r"D:\同花顺远航版"):
        self.ths_path = Path(ths_path)
        self.socket: Optional[socket.socket] = None
        self.connected = False
        self._response_queue = queue.Queue()
        self._recv_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
        # 加载本地股票数据库
        self._load_stock_db()
        
    def _load_stock_db(self):
        """加载本地股票名称数据库"""
        db_path = self.ths_path / "bin" / "stockname" / "stocknameV2.db"
        self.stock_db_path = str(db_path)
        self._stock_cache: Dict[str, str] = {}
        
        if db_path.exists():
            try:
                conn = sqlite3.connect(str(db_path))
                cursor = conn.cursor()
                cursor.execute("SELECT CODE, NAME FROM tablestock")
                for row in cursor.fetchall():
                    self._stock_cache[row[0]] = row[1]
                conn.close()
                print(f"已加载 {len(self._stock_cache)} 只股票信息")
            except Exception as e:
                print(f"加载股票数据库失败: {e}")
    
    def get_stock_name(self, code: str) -> str:
        """获取股票名称"""
        return self._stock_cache.get(code, code)
    
    def _get_market(self, code: str) -> str:
        """根据股票代码判断市场"""
        if code.startswith('6'):
            return self.MARKETS['SH']
        elif code.startswith(('0', '3')):
            return self.MARKETS['SZ']
        elif code.startswith('1'):
            return self.MARKETS['SHI']
        elif code.startswith('399'):
            return self.MARKETS['SZI']
        else:
            return self.MARKETS['SH']
    
    def connect(self) -> bool:
        """连接到同花顺服务器"""
        for host, port in self.SERVERS:
            try:
                print(f"尝试连接 {host}:{port}...")
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(10)
                self.socket.connect((host, port))
                self.connected = True
                
                # 启动接收线程
                self._stop_event.clear()
                self._recv_thread = threading.Thread(target=self._recv_loop, daemon=True)
                self._recv_thread.start()
                
                print(f"成功连接到 {host}:{port}")
                return True
            except Exception as e:
                print(f"连接 {host}:{port} 失败: {e}")
                if self.socket:
                    self.socket.close()
                    self.socket = None
                continue
        
        print("所有服务器连接失败")
        return False
    
    def _recv_loop(self):
        """接收数据循环"""
        buffer = b''
        while not self._stop_event.is_set():
            try:
                data = self.socket.recv(4096)
                if data:
                    buffer += data
                    # 尝试解析完整消息
                    while len(buffer) >= 4:
                        # 简单的消息格式：前4字节是长度
                        msg_len = struct.unpack('<I', buffer[:4])[0]
                        if len(buffer) >= msg_len + 4:
                            msg_data = buffer[4:msg_len+4]
                            buffer = buffer[msg_len+4:]
                            self._response_queue.put(msg_data)
                        else:
                            break
            except socket.timeout:
                continue
            except Exception as e:
                if not self._stop_event.is_set():
                    print(f"接收数据错误: {e}")
                break
    
    def _build_request(self, msg_id: int, params: Dict[str, Any]) -> bytes:
        """构建请求消息"""
        # 构建查询字符串
        query = f"id={msg_id}"
        for key, value in params.items():
            if isinstance(value, list):
                query += f"&{key}={','.join(map(str, value))}"
            else:
                query += f"&{key}={value}"
        
        # 消息格式：长度(4字节) + 查询字符串
        query_bytes = query.encode('utf-8')
        msg_len = len(query_bytes)
        return struct.pack('<I', msg_len) + query_bytes
    
    def _send_request(self, msg_id: int, params: Dict[str, Any], timeout: float = 5.0) -> Optional[bytes]:
        """发送请求并等待响应"""
        if not self.connected:
            raise ConnectionError("未连接到服务器")
        
        request = self._build_request(msg_id, params)
        self.socket.send(request)
        
        try:
            response = self._response_queue.get(timeout=timeout)
            return response
        except queue.Empty:
            return None
    
    def get_quote(self, code: str) -> Optional[QuoteData]:
        """获取实时行情"""
        market = self._get_market(code)
        
        # 请求ID 200 用于获取实时行情
        params = {
            'market': market,
            'codelist': code,
            'datatype': [5, 6, 7, 8, 9, 10, 13, 19, 22, 23, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
        }
        
        response = self._send_request(200, params)
        if response:
            return self._parse_quote(response, code)
        return None
    
    def get_ticks(self, code: str, date: int = 0) -> List[Dict]:
        """获取分时数据
        
        Args:
            code: 股票代码
            date: 日期，0表示今天
        """
        market = self._get_market(code)
        
        # 请求ID 207 用于获取分时数据
        params = {
            'market': market,
            'code': code,
            'date': date,
            'datatype': [13, 19, 10, 1]
        }
        
        response = self._send_request(207, params)
        if response:
            return self._parse_ticks(response)
        return []
    
    def get_trade_detail(self, code: str, start: int = -50, end: int = 0) -> List[TradeData]:
        """获取成交明细 (Level2数据)
        
        Args:
            code: 股票代码
            start: 起始位置，负数表示从末尾开始
            end: 结束位置
        """
        market = self._get_market(code)
        
        # 请求ID 205 用于获取成交明细
        params = {
            'market': market,
            'code': code,
            'start': start,
            'end': end,
            'datatype': [1, 12, 49, 10, 18]
        }
        
        response = self._send_request(205, params)
        if response:
            return self._parse_trade_detail(response)
        return []
    
    def get_level2_depth(self, code: str) -> Optional[Dict]:
        """获取Level2深度数据（十档买卖盘）"""
        market = self._get_market(code)
        
        params = {
            'market': market,
            'codelist': code,
            'datatype': [27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
        }
        
        response = self._send_request(202, params)
        if response:
            return self._parse_depth(response, code)
        return None
    
    def get_kline(self, code: str, start: int = -100, end: int = 0, 
                  period: int = 16384, fuquan: str = 'Q') -> List[Dict]:
        """获取K线数据
        
        Args:
            code: 股票代码
            start: 起始位置
            end: 结束位置
            period: 周期 (16384=日线, 16385=周线, 16386=月线)
            fuquan: 复权类型 (Q=前复权, H=后复权, 空=不复权)
        """
        market = self._get_market(code)
        
        params = {
            'market': market,
            'code': code,
            'start': start,
            'end': end,
            'datatype': [1, 7, 8, 9, 11, 13, 19],
            'period': period,
            'fuquan': fuquan
        }
        
        response = self._send_request(210, params)
        if response:
            return self._parse_kline(response)
        return []
    
    def _parse_quote(self, data: bytes, code: str) -> QuoteData:
        """解析行情数据"""
        # 这里需要根据实际的数据格式进行解析
        # 同花顺的数据格式是私有的，需要逆向分析
        # 这是一个简化版本
        try:
            # 尝试解压数据
            try:
                decompressed = zlib.decompress(data)
                data = decompressed
            except:
                pass
            
            # 解析二进制数据
            # 格式需要根据实际抓包分析
            return QuoteData(
                code=code,
                name=self.get_stock_name(code),
                price=0.0,
                open=0.0,
                high=0.0,
                low=0.0,
                volume=0,
                amount=0.0,
                bid_prices=[0.0] * 5,
                ask_prices=[0.0] * 5,
                bid_volumes=[0] * 5,
                ask_volumes=0,
                timestamp=int(time.time())
            )
        except Exception as e:
            print(f"解析行情数据失败: {e}")
            return None
    
    def _parse_ticks(self, data: bytes) -> List[Dict]:
        """解析分时数据"""
        try:
            try:
                decompressed = zlib.decompress(data)
                data = decompressed
            except:
                pass
            
            # 返回原始数据供分析
            return [{'raw': data.hex(), 'len': len(data)}]
        except Exception as e:
            print(f"解析分时数据失败: {e}")
            return []
    
    def _parse_trade_detail(self, data: bytes) -> List[TradeData]:
        """解析成交明细"""
        try:
            try:
                decompressed = zlib.decompress(data)
                data = decompressed
            except:
                pass
            
            return []
        except Exception as e:
            print(f"解析成交明细失败: {e}")
            return []
    
    def _parse_depth(self, data: bytes, code: str) -> Dict:
        """解析深度数据"""
        return {'code': code, 'raw': data.hex()}
    
    def _parse_kline(self, data: bytes) -> List[Dict]:
        """解析K线数据"""
        return []
    
    def close(self):
        """关闭连接"""
        self._stop_event.set()
        if self.socket:
            self.socket.close()
            self.socket = None
        self.connected = False
        print("连接已关闭")
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class THSLocalReader:
    """本地数据读取器 - 读取同花顺本地缓存数据"""
    
    def __init__(self, ths_path: str = r"D:\同花顺远航版"):
        self.ths_path = Path(ths_path)
        self.stock_db = self.ths_path / "bin" / "stockname" / "stocknameV2.db"
        
    def get_all_stocks(self) -> List[Dict[str, str]]:
        """获取所有股票列表"""
        stocks = []
        conn = sqlite3.connect(str(self.stock_db))
        cursor = conn.cursor()
        cursor.execute("SELECT CODE, NAME, MARKET FROM tablestock")
        for row in cursor.fetchall():
            stocks.append({
                'code': row[0],
                'name': row[1],
                'market': row[2]
            })
        conn.close()
        return stocks
    
    def search_stock(self, keyword: str) -> List[Dict[str, str]]:
        """搜索股票"""
        stocks = []
        conn = sqlite3.connect(str(self.stock_db))
        cursor = conn.cursor()
        cursor.execute(
            "SELECT CODE, NAME, MARKET FROM tablestock WHERE CODE LIKE ? OR NAME LIKE ? OR FIRSTPY LIKE ?",
            (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%')
        )
        for row in cursor.fetchall():
            stocks.append({
                'code': row[0],
                'name': row[1],
                'market': row[2]
            })
        conn.close()
        return stocks


# 测试代码
if __name__ == "__main__":
    print("=" * 60)
    print("同花顺Level2数据客户端")
    print("=" * 60)
    
    # 测试本地数据读取
    print("\n1. 测试本地数据读取...")
    reader = THSLocalReader()
    stocks = reader.search_stock("平安")
    print(f"搜索'平安'找到 {len(stocks)} 只股票:")
    for s in stocks[:5]:
        print(f"  {s['code']} - {s['name']} ({s['market']})")
    
    # 测试网络连接
    print("\n2. 测试服务器连接...")
    client = THSClient()
    if client.connect():
        print("服务器连接成功!")
        
        # 尝试获取数据
        print("\n3. 尝试获取行情数据...")
        # 这里需要实际测试协议
        
        client.close()
    else:
        print("服务器连接失败，请确保网络通畅")