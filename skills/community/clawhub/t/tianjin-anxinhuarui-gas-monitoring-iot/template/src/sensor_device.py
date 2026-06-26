# -*- coding: utf-8 -*-
"""
传感器设备管理模块
封装传感器状态读取、浓度数据读取逻辑
"""
import utime
from modbus_rtu import ModbusRTU


class SensorDevice:
    """单个传感器设备类"""
    
    # 传感器状态定义
    STATE_NORMAL = 0           # 正常
    STATE_LOW_ALARM = 2        # 低报警
    STATE_HIGH_ALARM = 3       # 高报警
    STATE_COM_ERROR = 7        # 通讯错误
    STATE_SENSOR_FAIL = 4      # 传感器故障
    
    def __init__(self, index, addr, modbus_engine):
        """
        初始化传感器
        
        参数:
            index: 传感器序号 (1-based)
            addr: Modbus 地址 (0-based)
            modbus_engine: Modbus 通信引擎实例
        """
        self.index = index
        self.addr = addr
        self.modbus = modbus_engine
        
        # 状态标志
        self.level_1_alarm = 0    # 低报警
        self.level_2_alarm = 0    # 高报警
        self.com_error = 0        # 通讯错误
        self.sensor_fail = 0      # 传感器故障
        self.sensor_ifblind = 0   # 盲点
        
        # 浓度数据
        self.dense = 0
        self.error_code = 0
    
    def read_status(self):
        """
        读取传感器状态
        
        返回:
            bool: 成功返回 True
        """
        result = self.modbus.read_registers(1, 2000 + self.addr, 1)
        
        if result['error'] != 0 or len(result['data']) < 1:
            self.com_error = 1
            return False
        
        status_value = result['data'][0]
        
        # 解析状态值
        if status_value == 0:
            # 正常
            self.level_1_alarm = 0
            self.level_2_alarm = 0
            self.com_error = 0
            self.sensor_fail = 0
        elif status_value == 2:
            self.level_1_alarm = 1
        elif status_value == 3:
            self.level_2_alarm = 1
        elif status_value == 4:
            self.sensor_fail = 1
        elif status_value == 5:
            # 通讯错误
            return False
        elif status_value == 7:
            self.com_error = 1
        
        return True
    
    def read_density(self):
        """
        读取传感器浓度值
        
        返回:
            bool: 成功返回 True
        """
        result = self.modbus.read_registers(1, 1000 + self.addr, 1)
        
        if result['error'] != 0 or len(result['data']) < 1:
            self.error_code = 1
            return False
        
        self.dense = result['data'][0]
        self.error_code = 0
        return True
    
    def to_dict(self):
        """
        转换为字典格式
        
        返回:
            dict: 传感器状态字典
        """
        return {
            'sensor_index': self.index,
            'sensor_addr': self.addr,
            'level_1_alarm': self.level_1_alarm,
            'level_2_alarm': self.level_2_alarm,
            'com_error': self.com_error,
            'sensor_fail': self.sensor_fail,
            'sensor_ifblind': self.sensor_ifblind,
            'error_code': self.error_code
        }
    
    def to_density_dict(self):
        """
        转换为浓度数据字典
        
        返回:
            dict: 浓度数据字典
        """
        return {
            'sensor_index': self.index,
            'sensor_addr': self.addr,
            'error_code': self.error_code,
            'sensor_dense': self.dense
        }


class SensorManager:
    """传感器管理器 - 管理所有传感器"""
    
    def __init__(self, modbus_engine, max_count=32):
        """
        初始化传感器管理器
        
        参数:
            modbus_engine: Modbus 通信引擎
            max_count: 最大传感器数量
        """
        self.modbus = modbus_engine
        self.max_count = max_count
        self.sensors = []
        
        # 初始化传感器列表
        for i in range(max_count):
            sensor = SensorDevice(index=i + 1, addr=i, modbus_engine=modbus_engine)
            self.sensors.append(sensor)
    
    def scan_sensors(self, retry_times=1, max_retry=5):
        """
        扫描所有在线传感器
        
        参数:
            retry_times: 当前重试次数
            max_retry: 最大重试次数
            
        返回:
            list: 在线传感器状态列表
        """
        online_sensors = []
        
        for sensor in self.sensors:
            if sensor.read_status():
                online_sensors.append(sensor.to_dict())
        
        # 如果读取失败且未达到最大重试次数，递归重试
        if len(online_sensors) == 0 and retry_times < max_retry:
            utime.sleep(1)
            return self.scan_sensors(retry_times + 1, max_retry)
        
        return online_sensors
    
    def read_all_density(self, sensor_list, retry_times=1, max_retry=5):
        """
        读取所有传感器的浓度值
        
        参数:
            sensor_list: 传感器状态列表
            retry_times: 当前重试次数
            max_retry: 最大重试次数
            
        返回:
            list: 浓度数据列表
        """
        density_list = []
        
        for sensor_data in sensor_list:
            addr = sensor_data['sensor_addr']
            sensor = self.sensors[addr]
            
            if sensor.read_density():
                density_list.append(sensor.to_density_dict())
            else:
                # 读取失败
                if retry_times < max_retry:
                    utime.sleep(1)
                    return self.read_all_density(sensor_list, retry_times + 1, max_retry)
                else:
                    return []
        
        return density_list
    
    def get_alarm_status(self, sensor_list):
        """
        检查是否有报警
        
        参数:
            sensor_list: 传感器状态列表
            
        返回:
            tuple: (has_alarm, has_fail, gas_sensor_state)
                   gas_sensor_state: 0=正常，1=高报，2=低报
        """
        has_alarm = 0
        has_fail = 0
        gas_sensor_state = 0
        
        for sensor in sensor_list:
            if sensor['level_1_alarm'] > 0 or sensor['level_2_alarm'] > 0:
                has_alarm = 1
            if sensor['com_error'] > 0 or sensor['sensor_fail'] > 0:
                has_fail = 1
            
            # 气体传感器状态 (高报优先)
            if sensor['level_2_alarm'] > 0:
                gas_sensor_state = 1  # 高报
                break
            elif sensor['level_1_alarm'] > 0:
                gas_sensor_state = 2  # 低报
        
        return has_alarm, has_fail, gas_sensor_state
