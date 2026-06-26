# -*- coding: utf-8 -*-
"""
数据上报模块
负责 HTTP 请求、数据打包、OTA 升级等
"""
import utime
import ujson
import request
import app_fota
from misc import Power


class DataReporter:
    """数据上报类"""
    
    def __init__(self, url_report, url_ota, led_net):
        """
        初始化数据上报
        
        参数:
            url_report: 数据上报 URL
            url_ota: OTA 升级 URL
            led_net: 网络 LED 实例
        """
        self.url_report = url_report
        self.url_ota = url_ota
        self.led_net = led_net
        self.server_fail_count = 0
    
    def post(self, body, url, description=""):
        """
        发送 HTTP POST 请求
        
        参数:
            body: 请求体 (JSON 字符串)
            url: 目标 URL
            description: 描述信息
            
        返回:
            int: 0=成功，-1=失败
        """
        self.led_net.off()
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = request.post(url, data=body, headers=headers)
            
            if response.status_code == 200:
                # 闪烁 LED 表示成功
                self.led_net.flash(0.25, 0.25, 8)
                self.led_net.on()
                
                # 解析响应
                for chunk in response.text:
                    try:
                        return_json = ujson.loads(chunk)
                        
                        # 检查是否有 OTA 升级
                        if return_json.get('code') == 200:
                            file_list = return_json.get('file_list', [])
                            if file_list:
                                self.run_ota(file_list)
                    except:
                        pass
                
                return 0
            else:
                print("HTTP 错误，状态码:", response.status_code)
                return -1
                
        except Exception as e:
            print("HTTP 请求异常:", e)
            return -1
    
    def run_ota(self, file_list):
        """
        执行 OTA 升级
        
        参数:
            file_list: 文件列表
        """
        print("*** 开始 OTA 升级 ***")
        print("升级文件:", file_list)
        try:
            fota = app_fota.new()
            fota.bulk_download(file_list)
            fota.set_update_flag()
            Power.powerRestart()
        except Exception as e:
            print("OTA 升级失败:", e)
    
    def report_sensor_data(self, net_info, sensor_stat, sensor_dens, sys_stat):
        """
        上报传感器数据
        
        参数:
            net_info: 网络信息
            sensor_stat: 传感器状态列表
            sensor_dens: 传感器浓度列表
            sys_stat: 系统状态
            
        返回:
            int: 0=成功，-1=失败
        """
        local_time = utime.localtime()
        timestamp = utime.mktime(local_time)
        time_str = "{}-{}-{} {}:{}:{}".format(
            local_time[0], local_time[1], local_time[2],
            local_time[3], local_time[4], local_time[5]
        )
        
        # 计算错误码
        error_code = 0
        if sys_stat.get('has_alarm', 0) > 0:
            error_code = 1
        elif sys_stat.get('has_fail', 0) > 0:
            error_code = 5
        elif sys_stat.get('back_power_fail', 0) > 0:
            error_code = 9
        
        # 计算气体传感器状态
        gas_sensor_state = 0
        for sensor in sensor_stat:
            if sensor.get('level_2_alarm', 0) > 0:
                gas_sensor_state = 1  # 高报
                break
            elif sensor.get('level_1_alarm', 0) > 0:
                gas_sensor_state = 2  # 低报
        
        # 构建上报数据体
        body = {
            'id': timestamp,
            'time': time_str,
            'unit_code': net_info.get('IMEI', ''),
            'sys_stat': sys_stat,
            'max_sensor_login_count': len(sensor_stat),
            'sensor_capacity': len(sensor_stat),
            'sensor_stat': sensor_stat,
            'sensor_dens': sensor_dens,
            'union_ctl_stat': {
                'wind_union_ctl': 0,
                'ac220_n_o_val_union': 0,
                'low_alarm_union': 0,
                'high_alarm_union': 0,
                'dc24_n_o_val_union': 0
            },
            'collections': {
                'signal_power': net_info.get('signal_power', 0),
                'cell_id': net_info.get('cell_id', 0),
                'ecl': net_info.get('ecl', 0),
                'pci': net_info.get('pci', 0),
                'sinr': net_info.get('sinr', 0),
                'rsrp': net_info.get('rsrp', 0),
                'manufacturer_name': '天津安信华瑞',
                'terminal_type': 'tuoan',
                'IMEI': net_info.get('IMEI', ''),
                'IMSI': net_info.get('IMSI', ''),
                'manufacturer_id': '18513099902',
                'medium': 0,
                'error_code': error_code,
                'valve_state': 0,
                'fan_state': 0,
                'gas_sensor_state': gas_sensor_state,
                'saas_version': '20231213'
            }
        }
        
        json_body = ujson.dumps(body)
        print("上报数据:", json_body[:200], "...")
        return self.post(json_body, self.url_report, "传感器数据")
    
    def report_boot_info(self, net_info, manufacturer, terminal_type, project_name, project_version):
        """
        上报设备启动信息 (用于 OTA 检查)
        
        参数:
            net_info: 网络信息
            manufacturer: 厂商名称
            terminal_type: 终端类型
            project_name: 项目名称
            project_version: 项目版本
            
        返回:
            int: 0=成功，-1=失败
        """
        local_time = utime.localtime()
        time_str = "{}-{}-{} {}:{}:{}".format(
            local_time[0], local_time[1], local_time[2],
            local_time[3], local_time[4], local_time[5]
        )
        
        body = {
            'time': time_str,
            'ts': utime.mktime(local_time),
            'imei': net_info.get('IMEI', ''),
            'imsi': net_info.get('IMSI', ''),
            'manu': manufacturer,
            'product': terminal_type,
            'project': project_name,
            'softver': project_version
        }
        
        json_body = ujson.dumps(body)
        print("上报启动信息")
        return self.post(json_body, self.url_ota, "启动信息")
