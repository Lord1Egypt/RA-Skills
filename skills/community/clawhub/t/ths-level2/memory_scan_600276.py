# -*- coding: utf-8 -*-
"""
通过内存读取恒瑞医药(600276) Level2数据
需要管理员权限运行
"""
import os
import sys
import ctypes
import ctypes.wintypes as wintypes
import struct

os.environ['PYTHONIOENCODING'] = 'utf-8'

# Windows API
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

# 常量
PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400
MEM_COMMIT = 0x1000
PAGE_READWRITE = 0x04

print("=" * 70)
print(" 内存读取恒瑞医药(600276) Level2数据")
print("=" * 70)

PID = 21152
print(f"\n连接进程 PID={PID}...")

handle = kernel32.OpenProcess(
    PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, PID
)

if not handle or handle == -1:
    print("打开进程失败，请以管理员权限运行!")
    sys.exit(1)

print("成功打开进程!")

def read_memory(h_process, address, size):
    buffer = ctypes.create_string_buffer(size)
    bytes_read = ctypes.c_size_t()
    success = kernel32.ReadProcessMemory(
        h_process, ctypes.c_void_p(address), buffer, size, ctypes.byref(bytes_read)
    )
    if success and bytes_read.value == size:
        return buffer.raw
    return None

print("\n扫描内存查找 '600276' ...")

class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_void_p),
        ("AllocationBase", ctypes.c_void_p),
        ("AllocationProtect", wintypes.DWORD),
        ("RegionSize", ctypes.c_size_t),
        ("State", wintypes.DWORD),
        ("Protect", wintypes.DWORD),
        ("Type", wintypes.DWORD),
    ]

mbi = MEMORY_BASIC_INFORMATION()
mbi_size = ctypes.sizeof(mbi)
address = 0
found = []

while address < 0x7FFFFFFF and len(found) < 20:
    result = kernel32.VirtualQueryEx(handle, ctypes.c_void_p(address), ctypes.byref(mbi), mbi_size)
    if result != mbi_size or mbi.BaseAddress is None:
        break
    
    if mbi.State == MEM_COMMIT and mbi.RegionSize:
        try:
            size = min(mbi.RegionSize, 1024*1024)
            data = read_memory(handle, mbi.BaseAddress, size)
            if data:
                pos = 0
                while True:
                    pos = data.find(b'600276', pos)
                    if pos == -1:
                        break
                    found.append(mbi.BaseAddress + pos)
                    print(f"  找到 0x{mbi.BaseAddress + pos:X}")
                    pos += 1
                    if len(found) >= 20:
                        break
        except:
            pass
    
    address = mbi.BaseAddress + mbi.RegionSize

print(f"\n共找到 {len(found)} 个位置")

if found:
    print("\n分析第一个位置的数据结构...")
    data = read_memory(handle, found[0] - 32, 128)
    if data:
        print(f"  原始数据: {data.hex()}")
        
        # 尝试解析浮点数
        print("\n  可能的价格数据:")
        for i in range(0, 128-4, 4):
            val = struct.unpack('<f', data[i:i+4])[0]
            if 10 < val < 200:
                print(f"    偏移{i-32}: {val:.2f}")

kernel32.CloseHandle(handle)
print("\n内存扫描完成")