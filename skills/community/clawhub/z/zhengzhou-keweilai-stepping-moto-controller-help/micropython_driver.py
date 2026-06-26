"""
郑州科威莱步进电机控制器 MicroPython 驱动
适用于 ESP32/Pico/RP2040 等开发板

河北雄安素水互联网科技有限公司
联系人：王建存
电话：18510412016
"""

from machine import UART
import struct
import time

class KeweilaiStepMotor:
    """郑州科威莱步进电机控制器 MicroPython 驱动类"""
    
    # ========== 寄存器地址定义 ==========
    REG_DIRECTION = 1       # 运行方向 (0=左，1=右)
    REG_RUN_CMD = 2         # 运行命令 (1=启动，0=停止)
    REG_ESTOP = 3           # 紧急停止 (1=停止)
    REG_SPEED = 4           # 运动速度 (1-800 r/min)
    REG_PULSES = 5          # 批量脉冲数
    REG_REVOLUTIONS = 6     # 批量圈数
    REG_ANGLE = 7           # 批量旋转角度 (增量模式)
    REG_MODBUS_ADDR = 8     # Modbus 地址
    REG_IDLE_ENABLE = 9     # 脱机使能
    REG_HOME = 10           # 一键回原点
    REG_POWER_HOME = 11     # 上电回原点
    REG_HOME_DIR = 12       # 上电回原点方向
    REG_LIMIT_ENABLE = 13   # 限位开关使能
    REG_ACCEL = 14          # 加减速系数 (0-10)
    REG_BAUDRATE = 15       # 波特率设置
    REG_AUTO_REPORT = 16    # 自动上报使能
    REG_SET_ORIGIN = 21     # 设当前位置为原点
    REG_POSITION = 22       # 已运行角度
    REG_LIMIT_STATUS = 23   # 限位开关状态
    
    # ========== 限位状态 ==========
    LIMIT_NONE = 0      # 无限位触发
    LIMIT_FORWARD = 1   # 正转限位 (终止位)
    LIMIT_REVERSE = 2   # 反转限位 (起始位/机械原点)
    
    # ========== 换算参数 ==========
    MM_PER_REV = 5.0        # 每圈毫米数
    DEG_PER_REV = 360.0     # 每圈角度
    DEG_PER_MM = 72.0       # 每毫米角度
    
    def __init__(self, uart_id, tx_pin, rx_pin, baudrate=9600, 
                 device_addr=9, timeout=1):
        """
        初始化步进电机控制器
        
        参数:
            uart_id: UART 编号 (0, 1, 2)
            tx_pin: TX 引脚编号
            rx_pin: RX 引脚编号
            baudrate: 波特率 (默认 9600)
            device_addr: 设备地址 (默认 9)
            timeout: 超时时间 (秒)
        """
        self.uart = UART(uart_id, baudrate=baudrate, tx=tx_pin, rx=rx_pin)
        self.device_addr = device_addr
        self.timeout = timeout
        time.sleep(0.1)
    
    # ========== CRC16 计算 ==========
    def _calculate_crc16(self, data):
        """计算 Modbus CRC16"""
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return crc
    
    # ========== 底层通讯 ==========
    def _send_request(self, frame):
        """发送请求并读取响应"""
        self.uart.write(frame)
        time.sleep_ms(50)
        
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < self.timeout * 1000:
            if self.uart.any() >= 5:
                return self.uart.read(self.uart.any())
            time.sleep_ms(10)
        
        return None
    
    def _verify_crc(self, data):
        """验证 CRC"""
        if len(data) < 2:
            return False
        received_crc = (data[-1] << 8) | data[-2]
        calculated_crc = self._calculate_crc16(data[:-2])
        return received_crc == calculated_crc
    
    # ========== 寄存器读取 ==========
    def read_register(self, addr):
        """
        读取单个寄存器 (功能码 03)
        
        参数:
            addr: 寄存器地址
        
        返回:
            寄存器值 (int)，失败返回 None
        """
        frame = bytearray([
            self.device_addr,
            0x03,
            (addr >> 8) & 0xFF,
            addr & 0xFF,
            0x00,
            0x01
        ])
        
        crc = self._calculate_crc16(frame)
        frame.append(crc & 0xFF)
        frame.append((crc >> 8) & 0xFF)
        
        response = self._send_request(frame)
        
        if not response or len(response) < 7:
            return None
        
        if response[0] != self.device_addr or response[1] != 0x03:
            return None
        
        if not self._verify_crc(response):
            return None
        
        value = (response[3] << 8) | response[4]
        return value
    
    def read_registers(self, addr, count):
        """
        读取多个寄存器 (功能码 03)
        
        参数:
            addr: 起始寄存器地址
            count: 读取数量
        
        返回:
            寄存器值列表，失败返回 None
        """
        frame = bytearray([
            self.device_addr,
            0x03,
            (addr >> 8) & 0xFF,
            addr & 0xFF,
            (count >> 8) & 0xFF,
            count & 0xFF
        ])
        
        crc = self._calculate_crc16(frame)
        frame.append(crc & 0xFF)
        frame.append((crc >> 8) & 0xFF)
        
        response = self._send_request(frame)
        
        if not response or len(response) < 7:
            return None
        
        if response[0] != self.device_addr or response[1] != 0x03:
            return None
        
        if not self._verify_crc(response):
            return None
        
        byte_count = response[2]
        data_bytes = response[3:3+byte_count]
        
        values = []
        for i in range(0, len(data_bytes), 2):
            value = (data_bytes[i] << 8) | data_bytes[i+1]
            values.append(value)
        
        return values
    
    # ========== 寄存器写入 ==========
    def write_register(self, addr, value):
        """
        写入单个寄存器 (功能码 06)
        
        参数:
            addr: 寄存器地址
            value: 写入值 (0-65535)
        
        返回:
            True=成功，False=失败
        """
        frame = bytearray([
            self.device_addr,
            0x06,
            (addr >> 8) & 0xFF,
            addr & 0xFF,
            (value >> 8) & 0xFF,
            value & 0xFF
        ])
        
        crc = self._calculate_crc16(frame)
        frame.append(crc & 0xFF)
        frame.append((crc >> 8) & 0xFF)
        
        response = self._send_request(frame)
        
        if not response or len(response) < 8:
            return False
        
        if response[0] != self.device_addr or response[1] != 0x06:
            return False
        
        if not self._verify_crc(response):
            return False
        
        return True
    
    # ========== 控制功能 ==========
    def set_direction(self, direction):
        """
        设置运行方向
        
        参数:
            direction: 1=向右 (正向)，0=向左 (反向)
        
        返回:
            True=成功，False=失败
        """
        return self.write_register(self.REG_DIRECTION, 1 if direction else 0)
    
    def start_run(self):
        """
        启动运行
        
        返回:
            True=成功，False=失败
        """
        return self.write_register(self.REG_RUN_CMD, 1)
    
    def stop_run(self):
        """
        停止运行 (正常停止，可能无效如果正在运行)
        
        返回:
            True=成功，False=失败
        """
        return self.write_register(self.REG_RUN_CMD, 0)
    
    def emergency_stop(self):
        """
        紧急停止 (立即停止)
        
        返回:
            True=成功，False=失败
        """
        return self.write_register(self.REG_ESTOP, 1)
    
    def set_speed(self, speed):
        """
        设置运动速度
        
        参数:
            speed: 速度 (1-800 r/min)
        
        返回:
            True=成功，False=失败
        """
        if speed < 1 or speed > 800:
            return False
        return self.write_register(self.REG_SPEED, speed)
    
    def set_angle(self, angle):
        """
        设置目标角度 (增量模式)
        
        参数:
            angle: 角度 (度)
        
        返回:
            True=成功，False=失败
        """
        return self.write_register(self.REG_ANGLE, int(angle))
    
    def set_distance_mm(self, mm):
        """
        设置目标距离 (毫米，自动转换为角度)
        
        参数:
            mm: 距离 (毫米)
        
        返回:
            True=成功，False=失败
        """
        angle = int(mm * self.DEG_PER_MM)
        return self.write_register(self.REG_ANGLE, angle)
    
    # ========== 原点功能 ==========
    def set_origin(self):
        """
        设定当前位置为原点
        
        返回:
            True=成功，False=失败
        """
        return self.write_register(self.REG_SET_ORIGIN, 1)
    
    def home_command(self):
        """
        执行回原点指令 (寄存器 10)
        
        返回:
            True=成功，False=失败
        """
        return self.write_register(self.REG_HOME, 1)
    
    def move_to_reverse_limit(self, max_angle=3600):
        """
        移动到反转限位 (机械原点)
        
        参数:
            max_angle: 最大移动角度 (默认 3600°)
        
        返回:
            True=成功，False=失败/超时
        """
        # 设置方向向左
        self.set_direction(0)
        time.sleep_ms(100)
        
        # 设置速度
        self.set_speed(50)
        time.sleep_ms(100)
        
        # 设置目标角度
        self.set_angle(max_angle)
        time.sleep_ms(100)
        
        # 启动运行
        self.start_run()
        
        # 等待反转限位触发
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < 60000:
            limit = self.read_register(self.REG_LIMIT_STATUS)
            if limit == self.LIMIT_REVERSE:
                # 紧急停止
                self.emergency_stop()
                time.sleep_ms(300)
                return True
            time.sleep_ms(300)
        
        self.emergency_stop()
        return False
    
    def mechanical_home(self):
        """
        完整机械原点设定流程
        
        返回:
            True=成功，False=失败
        """
        # 移动到反转限位
        if not self.move_to_reverse_limit():
            return False
        
        # 设定原点
        if not self.set_origin():
            return False
        
        # 等待 1 秒
        time.sleep(1)
        
        # 验证位置
        pos = self.read_register(self.REG_POSITION)
        return pos == 0
    
    # ========== 状态读取 ==========
    def get_position(self):
        """
        读取当前位置 (角度)
        
        返回:
            位置 (度)，失败返回 None
        """
        return self.read_register(self.REG_POSITION)
    
    def get_position_mm(self):
        """
        读取当前位置 (毫米)
        
        返回:
            位置 (mm)，失败返回 None
        """
        pos = self.get_position()
        if pos is None:
            return None
        return pos / self.DEG_PER_MM
    
    def get_limit_status(self):
        """
        读取限位状态
        
        返回:
            0=无限位，1=正转限位，2=反转限位，None=失败
        """
        return self.read_register(self.REG_LIMIT_STATUS)
    
    def get_speed(self):
        """
        读取当前速度
        
        返回:
            速度 (r/min)，失败返回 None
        """
        return self.read_register(self.REG_SPEED)
    
    def is_running(self):
        """
        检查是否正在运行
        
        返回:
            True=运行中，False=停止，None=读取失败
        """
        status = self.read_register(self.REG_RUN_CMD)
        if status is None:
            return None
        return status == 1
    
    def wait_motion_complete(self, timeout=60):
        """
        等待运动完成
        
        参数:
            timeout: 超时时间 (秒)
        
        返回:
            True=完成，False=超时
        """
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < timeout * 1000:
            if not self.is_running():
                time.sleep_ms(500)  # 确认稳定
                if not self.is_running():
                    return True
            time.sleep_ms(200)
        return False
    
    # ========== 毫米移动 ==========
    def move_mm(self, mm, direction=1, speed=100):
        """
        移动指定毫米数 (增量模式)
        
        参数:
            mm: 距离 (毫米)
            direction: 方向 (1=向右，0=向左)
            speed: 速度 (r/min)
        
        返回:
            True=成功，False=失败
        """
        # 设置方向
        self.set_direction(direction)
        time.sleep_ms(100)
        
        # 设置速度
        self.set_speed(speed)
        time.sleep_ms(100)
        
        # 设置距离
        if not self.set_distance_mm(mm):
            return False
        time.sleep_ms(100)
        
        # 启动运行
        if not self.start_run():
            return False
        
        # 等待完成
        return self.wait_motion_complete()
    
    # ========== 工具函数 ==========
    def mm_to_degrees(self, mm):
        """毫米转角度"""
        return mm * self.DEG_PER_MM
    
    def degrees_to_mm(self, degrees):
        """角度转毫米"""
        return degrees / self.DEG_PER_MM
    
    def test_connection(self):
        """测试设备连接"""
        addr = self.read_register(self.REG_MODBUS_ADDR)
        return addr == self.device_addr
    
    def get_all_status(self):
        """
        获取所有状态信息
        
        返回:
            字典包含所有状态
        """
        status = {}
        
        regs = self.read_registers(self.REG_DIRECTION, 23 - self.REG_DIRECTION + 1)
        if regs:
            status['direction'] = regs[0]  # 寄存器 1
            status['run_cmd'] = regs[1]    # 寄存器 2
            status['speed'] = regs[3]      # 寄存器 4
            status['angle'] = regs[6]      # 寄存器 7
            status['position'] = regs[21]  # 寄存器 22
            status['limit'] = regs[22]     # 寄存器 23
        
        return status


# ========== 使用示例 ==========
if __name__ == "__main__":
    print("=" * 50)
    print("郑州科威莱步进电机控制器 - MicroPython 示例")
    print("=" * 50)
    
    # 初始化 (根据实际引脚调整)
    # ESP32: uart_id=1, tx_pin=10, rx_pin=9
    # Pico:  uart_id=1, tx_pin=8, rx_pin=9
    motor = KeweilaiStepMotor(uart_id=1, tx_pin=8, rx_pin=9)
    
    # 测试连接
    print("\n[1] 测试连接...")
    if motor.test_connection():
        print("    [OK] 设备连接成功")
    else:
        print("    [FAIL] 设备连接失败")
    
    # 读取状态
    print("\n[2] 读取状态...")
    status = motor.get_all_status()
    print(f"    位置：{status.get('position', '?')}°")
    print(f"    速度：{status.get('speed', '?')} r/min")
    print(f"    限位：{status.get('limit', '?')}")
    
    # 示例：移动 6mm
    print("\n[3] 移动 6mm 示例...")
    print("    注意：请先执行机械原点设定流程")
    # motor.mechanical_home()  # 先回机械原点
    # motor.move_mm(6)  # 移动 6mm
    
    print("\n" + "=" * 50)
    print("示例结束")
    print("=" * 50)
