"""
同花顺Level2内存数据读取器

通过读取同花顺进程内存获取实时Level2数据
需要管理员权限运行
"""

import ctypes
import ctypes.wintypes as wintypes
import struct
import re
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass
import time

# Windows API 定义
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
psapi = ctypes.WinDLL('psapi', use_last_error=True)

# 常量
PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400
MEM_COMMIT = 0x1000
PAGE_READWRITE = 0x04
PAGE_EXECUTE_READWRITE = 0x40


@dataclass
class Level2Quote:
    """Level2行情数据"""
    code: str
    name: str
    price: float
    open: float
    high: float
    low: float
    pre_close: float
    volume: int
    amount: float
    
    # 五档买盘
    bid_price1: float
    bid_price2: float
    bid_price3: float
    bid_price4: float
    bid_price5: float
    bid_volume1: int
    bid_volume2: int
    bid_volume3: int
    bid_volume4: int
    bid_volume5: int
    
    # 五档卖盘
    ask_price1: float
    ask_price2: float
    ask_price3: float
    ask_price4: float
    ask_price5: float
    ask_volume1: int
    ask_volume2: int
    ask_volume3: int
    ask_volume4: int
    ask_volume5: int
    
    timestamp: int


class MemoryReader:
    """Windows内存读取器"""
    
    def __init__(self, process_id: int):
        self.pid = process_id
        self.handle = None
        
    def open(self) -> bool:
        """打开进程"""
        self.handle = kernel32.OpenProcess(
            PROCESS_VM_READ | PROCESS_QUERY_INFORMATION,
            False,
            self.pid
        )
        return self.handle is not None and self.handle != -1
    
    def close(self):
        """关闭进程句柄"""
        if self.handle:
            kernel32.CloseHandle(self.handle)
            self.handle = None
    
    def read_bytes(self, address: int, size: int) -> Optional[bytes]:
        """读取指定地址的字节"""
        if not self.handle:
            return None
            
        buffer = ctypes.create_string_buffer(size)
        bytes_read = ctypes.c_size_t()
        
        success = kernel32.ReadProcessMemory(
            self.handle,
            ctypes.c_void_p(address),
            buffer,
            size,
            ctypes.byref(bytes_read)
        )
        
        if success and bytes_read.value == size:
            return buffer.raw
        return None
    
    def read_float(self, address: int) -> Optional[float]:
        """读取浮点数"""
        data = self.read_bytes(address, 4)
        if data:
            return struct.unpack('<f', data)[0]
        return None
    
    def read_int(self, address: int) -> Optional[int]:
        """读取整数"""
        data = self.read_bytes(address, 4)
        if data:
            return struct.unpack('<i', data)[0]
        return None
    
    def read_double(self, address: int) -> Optional[float]:
        """读取双精度浮点数"""
        data = self.read_bytes(address, 8)
        if data:
            return struct.unpack('<d', data)[0]
        return None
    
    def read_string(self, address: int, max_len: int = 64, encoding: str = 'gbk') -> Optional[str]:
        """读取字符串"""
        data = self.read_bytes(address, max_len)
        if data:
            try:
                # 找到null终止符
                null_pos = data.find(b'\x00')
                if null_pos > 0:
                    data = data[:null_pos]
                return data.decode(encoding)
            except:
                return None
        return None
    
    def scan_memory(self, pattern: bytes, mask: str = None) -> List[int]:
        """扫描内存查找模式"""
        results = []
        
        # 枚举内存区域
        address = 0
        mbi = wintypes.MEMORY_BASIC_INFORMATION()
        mbi_size = ctypes.sizeof(mbi)
        
        while kernel32.VirtualQueryEx(
            self.handle,
            ctypes.c_void_p(address),
            ctypes.byref(mbi),
            mbi_size
        ) == mbi_size:
            
            if mbi.State == MEM_COMMIT and mbi.Protect in [PAGE_READWRITE, PAGE_EXECUTE_READWRITE]:
                # 读取这块内存
                try:
                    data = self.read_bytes(mbi.BaseAddress, mbi.RegionSize)
                    if data:
                        # 搜索模式
                        offset = 0
                        while True:
                            pos = data.find(pattern, offset)
                            if pos == -1:
                                break
                            results.append(mbi.BaseAddress + pos)
                            offset = pos + 1
                except:
                    pass
            
            address = mbi.BaseAddress + mbi.RegionSize
            if address >= 0x7FFFFFFF:  # 用户空间上限
                break
        
        return results


class THSMemoryReader:
    """同花顺内存数据读取"""
    
    def __init__(self):
        self.process_id: Optional[int] = None
        self.reader: Optional[MemoryReader] = None
        self.base_address: Optional[int] = None
        
    def find_process(self, process_name: str = "happ.exe") -> Optional[int]:
        """查找同花顺进程"""
        import subprocess
        
        try:
            # 使用tasklist查找进程
            result = subprocess.run(
                ['tasklist', '/FI', f'IMAGENAME eq {process_name}', '/FO', 'CSV', '/NH'],
                capture_output=True,
                text=True
            )
            
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if process_name.lower() in line.lower():
                    # 解析PID
                    parts = line.split(',')
                    if len(parts) >= 2:
                        pid = int(parts[1].strip('"'))
                        return pid
        except Exception as e:
            print(f"查找进程失败: {e}")
        
        return None
    
    def connect(self) -> bool:
        """连接到同花顺进程"""
        self.process_id = self.find_process()
        if not self.process_id:
            print("未找到同花顺进程，请确保同花顺正在运行")
            return False
        
        print(f"找到同花顺进程 PID: {self.process_id}")
        
        self.reader = MemoryReader(self.process_id)
        if self.reader.open():
            print("成功连接到同花顺进程")
            return True
        else:
            print("打开进程失败，请以管理员权限运行")
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.reader:
            self.reader.close()
            self.reader = None
    
    def find_stock_data(self, code: str) -> Optional[int]:
        """在内存中查找股票数据
        
        同花顺可能在内存中存储股票代码，我们可以通过搜索代码定位数据结构
        """
        if not self.reader:
            return None
        
        # 股票代码在内存中的表示（可能有多种编码）
        patterns = [
            code.encode('ascii'),           # ASCII
            code.encode('utf-8'),           # UTF-8
            code.encode('gbk'),             # GBK
        ]
        
        for pattern in patterns:
            addresses = self.reader.scan_memory(pattern)
            if addresses:
                print(f"找到 {code} 在 {len(addresses)} 个位置")
                for addr in addresses[:5]:
                    print(f"  0x{addr:X}")
                return addresses[0] if addresses else None
        
        return None
    
    def read_quote(self, code: str) -> Optional[Level2Quote]:
        """读取股票行情数据
        
        注意: 这个函数需要根据实际的内存结构进行调整
        需要使用调试工具（如x64dbg）分析具体的数据偏移
        """
        if not self.reader:
            return None
        
        # 查找股票数据地址
        base_addr = self.find_stock_data(code)
        if not base_addr:
            return None
        
        # 这里需要根据实际的内存结构读取数据
        # 以下是一个假设的结构，需要根据实际情况调整
        
        # 假设数据结构:
        # +0x00: 股票代码 (8字节)
        # +0x10: 股票名称 (32字节)
        # +0x30: 最新价 (4字节 float)
        # +0x34: 开盘价
        # +0x38: 最高价
        # +0x3C: 最低价
        # ... 等等
        
        try:
            # 这些偏移量需要通过逆向分析确定
            PRICE_OFFSET = 0x30
            OPEN_OFFSET = 0x34
            HIGH_OFFSET = 0x38
            LOW_OFFSET = 0x3C
            
            price = self.reader.read_float(base_addr + PRICE_OFFSET)
            open_price = self.reader.read_float(base_addr + OPEN_OFFSET)
            high = self.reader.read_float(base_addr + HIGH_OFFSET)
            low = self.reader.read_float(base_addr + LOW_OFFSET)
            
            return Level2Quote(
                code=code,
                name="",
                price=price or 0,
                open=open_price or 0,
                high=high or 0,
                low=low or 0,
                pre_close=0,
                volume=0,
                amount=0,
                bid_price1=0, bid_price2=0, bid_price3=0, bid_price4=0, bid_price5=0,
                bid_volume1=0, bid_volume2=0, bid_volume3=0, bid_volume4=0, bid_volume5=0,
                ask_price1=0, ask_price2=0, ask_price3=0, ask_price4=0, ask_price5=0,
                ask_volume1=0, ask_volume2=0, ask_volume3=0, ask_volume4=0, ask_volume5=0,
                timestamp=int(time.time())
            )
        except Exception as e:
            print(f"读取行情数据失败: {e}")
            return None
    
    def get_module_base(self, module_name: str) -> Optional[int]:
        """获取模块基址"""
        if not self.reader:
            return None
        
        # 枚举进程模块
        h_modules = (wintypes.HMODULE * 1024)()
        cb_needed = wintypes.DWORD()
        
        if psapi.EnumProcessModulesEx(
            self.reader.handle,
            h_modules,
            ctypes.sizeof(h_modules),
            ctypes.byref(cb_needed),
            0x03  # LIST_MODULES_ALL
        ):
            count = cb_needed.value // ctypes.sizeof(wintypes.HMODULE)
            
            for i in range(count):
                module_name_buf = ctypes.create_unicode_buffer(260)
                psapi.GetModuleBaseNameW(
                    self.reader.handle,
                    h_modules[i],
                    module_name_buf,
                    260
                )
                
                if module_name.lower() in module_name_buf.value.lower():
                    return h_modules[i]
        
        return None


# 另一种方法: 使用共享内存

class THSSharedMemory:
    """通过共享内存读取同花顺数据"""
    
    def __init__(self):
        self.handle = None
        self.buffer = None
        
    def find_shared_memory(self) -> List[str]:
        """查找可能的共享内存名称"""
        # 同花顺可能使用的共享内存名称模式
        patterns = [
            "THS_",
            "HEVO_",
            "Quote_",
            "Level2_",
            "Hithink_"
        ]
        
        # 在Windows中查找共享内存需要特殊工具
        # 这里返回可能的名称供参考
        return patterns
    
    def connect(self, name: str) -> bool:
        """连接到共享内存"""
        # 使用CreateFileMapping打开已存在的共享内存
        size = 1024 * 1024  # 1MB
        
        self.handle = kernel32.OpenFileMappingW(
            0x0004,  # FILE_MAP_READ
            False,
            name
        )
        
        if self.handle:
            self.buffer = kernel32.MapViewOfFile(
                self.handle,
                0x0004,  # FILE_MAP_READ
                0, 0, size
            )
            return self.buffer is not None
        
        return False
    
    def read_data(self, offset: int, size: int) -> Optional[bytes]:
        """读取共享内存数据"""
        if not self.buffer:
            return None
        
        data = ctypes.string_at(self.buffer + offset, size)
        return data


# 测试代码
if __name__ == "__main__":
    print("=" * 60)
    print("同花顺内存数据读取器")
    print("=" * 60)
    
    reader = THSMemoryReader()
    
    if reader.connect():
        print("\n尝试查找股票数据...")
        
        # 搜索常见股票
        test_codes = ['600000', '000001', '300033']
        for code in test_codes:
            print(f"\n查找 {code}...")
            addr = reader.find_stock_data(code)
            if addr:
                print(f"  找到地址: 0x{addr:X}")
        
        reader.disconnect()
    else:
        print("\n连接失败，请确保:")
        print("1. 同花顺正在运行")
        print("2. 以管理员权限运行此脚本")