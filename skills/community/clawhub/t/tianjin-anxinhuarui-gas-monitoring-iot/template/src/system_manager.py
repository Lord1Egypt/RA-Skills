# -*- coding: utf-8 -*-
"""
系统管理模块
负责看门狗、电源状态、系统状态计算等
"""
from machine import WDT
import utime


class SystemManager:
    """系统管理类"""
    
    # 电源状态常量
    POWER_OK = 0
    POWER_FAIL = 1
    
    # 设备主状态码
    STATE_NORMAL = 2           # 正常
    STATE_NO_SENSOR = 0x08     # 无传感器
    STATE_MAIN_POWER_FAIL = 0x11    # 主电故障
    STATE_BACK_POWER_FAIL = 0x12    # 备电故障
    STATE_HIGH_ALARM = 0x14    # 高报
    STATE_LOW_ALARM = 0x15     # 低报
    STATE_SENSOR_FAIL = 0x13   # 传感器故障
    
    def __init__(self, wdt_timeout_ms=320000):
        """
        初始化系统管理
        
        参数:
            wdt_timeout_ms: 看门狗超时时间 (毫秒)
        """
        self.wdt = WDT(320)  # 320 秒 = 约 5.3 分钟
        self.wdt_timeout_ms = wdt_timeout_ms
        self.last_feed_time = 0
    
    def feed_dog(self):
        """喂看门狗"""
        self.wdt.feed()
        self.last_feed_time = utime.mktime(utime.localtime())
        print("喂狗时间:", utime.localtime())
    
    def read_battery_status(self, modbus, retry_times=1, max_retry=5):
        """
        读取电池状态
        
        参数:
            modbus: Modbus 引擎
            retry_times: 当前重试次数
            max_retry: 最大重试次数
            
        返回:
            dict: {'back_power_fail': 0/1, 'main_power_fail': 0/1}
        """
        result = modbus.read_registers(1, 0, 1)
        
        if result['error'] != 0 or len(result['data']) < 1:
            if retry_times < max_retry:
                utime.sleep(1)
                return self.read_battery_status(modbus, retry_times + 1, max_retry)
            else:
                return {'back_power_fail': -1, 'main_power_fail': -1}
        
        battery_status = result['data'][0]
        
        # 解析电源状态
        if battery_status == 0:
            return {'back_power_fail': 0, 'main_power_fail': 0}
        elif battery_status == 256:
            return {'back_power_fail': 0, 'main_power_fail': 1}
        elif battery_status == 1:
            return {'back_power_fail': 1, 'main_power_fail': 0}
        elif battery_status == 257:
            return {'back_power_fail': 1, 'main_power_fail': 1}
        else:
            return {'back_power_fail': -1, 'main_power_fail': -1}
    
    def build_sys_stat(self, battery_stat, sensor_stat):
        """
        构建系统状态字典
        
        参数:
            battery_stat: 电池状态
            sensor_stat: 传感器状态列表
            
        返回:
            dict: 系统状态字典
        """
        sys_stat = dict(battery_stat)
        
        # 初始化所有状态字段
        sys_stat['has_alarm'] = 0
        sys_stat['has_fail'] = 0
        sys_stat['reset'] = 0
        sys_stat['power_on'] = 0
        sys_stat['back_power_on'] = 0
        sys_stat['back_power_low'] = 0
        sys_stat['main_chain_fail'] = 0
        sys_stat['has_blind'] = 0
        sys_stat['has_union'] = 0
        sys_stat['has_feedback'] = 0
        sys_stat['union_lock_if_manual'] = 0
        sys_stat['keyboard_if_allow'] = 0
        
        # 检查传感器报警和故障
        for sensor in sensor_stat:
            if sensor.get('level_1_alarm', 0) > 0 or sensor.get('level_2_alarm', 0) > 0:
                sys_stat['has_alarm'] = 1
            if sensor.get('com_error', 0) > 0 or sensor.get('sensor_fail', 0) > 0:
                sys_stat['has_fail'] = 1
        
        return sys_stat
    
    def calc_main_state(self, sensor_count, battery_stat, sensor_stat):
        """
        计算设备主状态码
        
        参数:
            sensor_count: 传感器数量
            battery_stat: 电池状态
            sensor_stat: 传感器状态列表
            
        返回:
            int: 主状态码
        """
        main_state = self.STATE_NORMAL
        
        # 无传感器登录
        if sensor_count == 0:
            main_state = self.STATE_NO_SENSOR
        
        # 电源故障优先
        if battery_stat.get('main_power_fail', 0) == 1:
            main_state = self.STATE_MAIN_POWER_FAIL
        elif battery_stat.get('back_power_fail', 0) == 1:
            main_state = self.STATE_BACK_POWER_FAIL
        
        # 检查传感器状态 (优先级：高报 > 低报 > 故障)
        for sensor in sensor_stat:
            if sensor.get('level_2_alarm', 0) == 1:
                main_state = self.STATE_HIGH_ALARM
                break
            elif sensor.get('level_1_alarm', 0) == 1:
                if main_state not in [self.STATE_HIGH_ALARM]:
                    main_state = self.STATE_LOW_ALARM
            elif sensor.get('com_error', 0) == 1:
                if main_state not in [self.STATE_HIGH_ALARM, self.STATE_LOW_ALARM, self.STATE_NO_SENSOR]:
                    main_state = self.STATE_NO_SENSOR
            elif sensor.get('sensor_fail', 0) == 1:
                if main_state not in [self.STATE_HIGH_ALARM, self.STATE_LOW_ALARM, self.STATE_SENSOR_FAIL]:
                    main_state = self.STATE_SENSOR_FAIL
        
        return main_state
    
    def build_sensor_data(self, sensor_stat, sensor_dens, net_info):
        """
        构建传感器数据 (旧格式兼容)
        
        参数:
            sensor_stat: 传感器状态列表
            sensor_dens: 传感器浓度列表
            net_info: 网络信息
            
        返回:
            dict: 传感器数据字典
        """
        # 计算主状态
        main_state = self.calc_main_state(
            len(sensor_stat),
            {'main_power_fail': 0, 'back_power_fail': 0},
            sensor_stat
        )
        
        # 构建控制器数据
        controller = {
            'type': 2,
            'device_id': net_info.get('IMEI', '')[-12:],
            'device_information': {
                'ccid': net_info.get('ccid', ''),
                'imei': net_info.get('IMEI', ''),
                'moduleType': 4,
                'programVersion': '10.16'
            },
            'device_operation': {
                'signal': net_info.get('signal_power', 0),
                'state': main_state
            },
            'real_time_data': {
                'cycle': 1,
                'cycle_unit': 2,
                'detector': [],
                'io': []
            },
            'mqtt': 0
        }
        
        # 添加传感器数据
        for stat_item in sensor_stat:
            state = 2  # 默认正常
            
            if stat_item.get('level_2_alarm', 0) == 1:
                state = 4
            elif stat_item.get('level_1_alarm', 0) == 1:
                state = 3
            elif stat_item.get('com_error', 0) == 1:
                state = 5
            elif stat_item.get('sensor_fail', 0) == 1:
                state = 13
            
            sensor_data = {
                'detector_number': stat_item['sensor_index'],
                'sensor': [{
                    'number': 1,
                    'sensorType': 11,
                    'sensorCon': 0,
                    'lowerLimit': 25,
                    'upperLimit': 50,
                    'rangeValue': 100,
                    'sensorUnit': 1,
                    'sensorPoint': 1,
                    'state': state
                }]
            }
            
            # 填充浓度值
            for dens_item in sensor_dens:
                if dens_item['sensor_addr'] == stat_item['sensor_addr']:
                    sensor_data['sensor'][0]['sensorCon'] = dens_item['sensor_dense']
                    break
            
            controller['real_time_data']['detector'].append(sensor_data)
        
        return controller
