# -*- coding: utf-8 -*-
"""
Modbus RTU 通信协议模块
支持 RTU 模式的 CRC 校验、寄存器读写操作
"""
from machine import UART
import ubinascii as binascii
import utime as time


class ModbusRTU:
    """Modbus RTU 通信类"""
    
    # Modbus 功能码常量
    FUNC_READ_COILS = 1
    FUNC_READ_DISCRETE = 2
    FUNC_READ_HOLDING = 3
    FUNC_READ_INPUT = 4
    FUNC_WRITE_COIL = 5
    FUNC_WRITE_REG = 6
    FUNC_WRITE_MULTI_COILS = 15
    FUNC_WRITE_MULTI_REGS = 16
    
    # 异常功能码偏移
    FUNC_EXCEPTION = 0x80
    
    def __init__(self, uart_num, baudrate=9600, databits=8, parity=0, stopbits=1, flowctl=0):
        """
        初始化 Modbus RTU
        
        参数:
            uart_num: UART 端口号
            baudrate: 波特率
            databits: 数据位
            parity: 校验位 (0=无校验)
            stopbits: 停止位
            flowctl: 流控制
        """
        self.uart = UART(uart_num, baudrate, databits, parity, stopbits, flowctl)
    
    @staticmethod
    def split_high_low(value):
        """
        将 16 位整数拆分为高低字节
        
        参数:
            value: 16 位整数
            
        返回:
            (high, low) 元组
        """
        high = (value >> 8) & 0xFF
        low = value & 0xFF
        return high, low
    
    def calc_crc(self, data):
        """
        计算 CRC16 校验码 (Modbus 标准)
        
        参数:
            data: bytearray 数据
            
        返回:
            (crc_low, crc_high) 元组
        """
        crc = 0xFFFF
        for pos in data:
            crc ^= pos
            for _ in range(8):
                if crc & 1:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        # Modbus CRC 低字节在前
        crc_low = crc & 0xFF
        crc_high = (crc >> 8) & 0xFF
        return crc_low, crc_high
    
    def read_response(self, timeout_ms=2000):
        """
        读取 UART 响应数据
        
        参数:
            timeout_ms: 超时时间 (毫秒)
            
        返回:
            十六进制字符串列表，失败返回空列表
        """
        max_wait = timeout_ms // 100
        for _ in range(max_wait):
            if self.uart.any() > 0:
                num = self.uart.any()
                msg = self.uart.read(num)
                hex_str = binascii.hexlify(msg, ",")
                return hex_str.split(b",")
            time.sleep_ms(100)
        return []
    
    def build_command(self, slave_addr, func_code, start_addr, data=None):
        """
        构建 Modbus 命令帧
        
        参数:
            slave_addr: 从站地址
            func_code: 功能码
            start_addr: 起始地址
            data: 数据列表或数量 (可选)
            
        返回:
            bytearray 命令帧
        """
        start_high, start_low = self.split_high_low(start_addr)
        
        if func_code == self.FUNC_WRITE_MULTI_REGS and data:
            # 写多个寄存器
            count = len(data) // 2
            count_high, count_low = self.split_high_low(count)
            cmd = bytearray([
                slave_addr, func_code,
                start_high, start_low,
                count_high, count_low,
                len(data)
            ])
            cmd.extend(data)
        elif func_code in [self.FUNC_READ_HOLDING, self.FUNC_READ_INPUT]:
            # 读寄存器 (data 此时是数量)
            count_high, count_low = self.split_high_low(data)
            cmd = bytearray([
                slave_addr, func_code,
                start_high, start_low,
                count_high, count_low
            ])
        else:
            cmd = bytearray([slave_addr, func_code, start_high, start_low])
        
        # 添加 CRC 校验
        crc_low, crc_high = self.calc_crc(cmd)
        cmd.append(crc_low)
        cmd.append(crc_high)
        
        return cmd
    
    def send_command(self, cmd):
        """
        发送 Modbus 命令
        
        参数:
            cmd: bytearray 命令帧
        """
        self.uart.write(cmd)
        time.sleep_ms(200)  # 等待响应
    
    def read_registers(self, slave_addr, start_addr, count):
        """
        读取保持寄存器
        
        参数:
            slave_addr: 从站地址
            start_addr: 起始地址
            count: 读取数量
            
        返回:
            dict: {'error': 错误码，'data': 数据列表}
                  错误码：0=成功，1=超时，2=异常响应，3=长度错误，4=数据错误，5=解析异常
        """
        result = {'error': 0, 'data': []}
        
        # 构建并发送命令
        cmd = self.build_command(slave_addr, self.FUNC_READ_HOLDING, start_addr, count)
        self.uart.write(cmd)
        time.sleep_ms(200)
        
        # 读取响应
        response = self.read_response()
        
        if not response:
            result['error'] = 1  # 超时
            return result
        
        try:
            # 检查从站地址
            resp_slave = int(response[0], 16)
            if resp_slave != slave_addr:
                result['error'] = 6  # 从站地址不匹配
                return result
            
            # 检查功能码
            func_return = int(response[1], 16)
            if func_return > 16:  # 异常响应 (功能码 + 0x80)
                result['error'] = 2
                return result
            
            # 检查数据长度 (地址 + 功能码 + 字节数 + 数据 + CRC)
            expected_len = count * 2 + 5
            if len(response) != expected_len:
                result['error'] = 3
                return result
            
            # 提取数据
            byte_count = int(response[2], 16)
            if byte_count != count * 2:
                result['error'] = 4
                return result
            
            # 解析数据 (跳过地址、功能码、字节数)
            for i in range(count):
                high = int(response[3 + i * 2], 16)
                low = int(response[3 + i * 2 + 1], 16)
                value = (high << 8) | low
                result['data'].append(value)
                
        except Exception as e:
            result['error'] = 5
            print("Modbus 解析错误:", e)
        
        return result
    
    def write_registers(self, slave_addr, start_addr, values):
        """
        写入多个寄存器
        
        参数:
            slave_addr: 从站地址
            start_addr: 起始地址
            values: 值列表
            
        返回:
            bool: 成功返回 True
        """
        # 将值转换为字节列表
        data_bytes = []
        for val in values:
            high, low = self.split_high_low(val)
            data_bytes.extend([high, low])
        
        cmd = self.build_command(slave_addr, self.FUNC_WRITE_MULTI_REGS, start_addr, data_bytes)
        self.uart.write(cmd)
        time.sleep_ms(200)
        return True
