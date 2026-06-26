# -*- coding: utf-8 -*-
"""
网络管理模块
负责网络连接、信号获取、时间同步等
"""
import utime
import ntptime
import net
import sim
import modem
import checkNet


class NetworkManager:
    """网络管理类"""
    
    def __init__(self, project_name, project_version):
        """
        初始化网络管理
        
        参数:
            project_name: 项目名称
            project_version: 项目版本
        """
        self.project_name = project_name
        self.project_version = project_version
        self.checknet = checkNet.CheckNetwork(project_name, project_version)
        self.net_error = 0
        self.net_info = {}
    
    def wait_connected(self, timeout=30):
        """
        等待网络连接
        
        参数:
            timeout: 超时时间 (秒)
            
        返回:
            bool: 连接成功返回 True
        """
        stage, state = self.checknet.wait_network_connected(timeout)
        sim_status = sim.getStatus()
        
        if stage == 3 and state == 1 and sim_status == 1:
            self.checknet.poweron_print_once()
            self.net_error = 0
            return True
        else:
            self.net_error = 1
            return False
    
    def sync_time(self, timezone=8):
        """
        同步 NTP 时间
        
        参数:
            timezone: 时区
        """
        try:
            ntptime.settime(timezone=timezone)
        except Exception as e:
            print("NTP 同步失败:", e)
    
    def get_signal_info(self):
        """
        获取信号强度信息
        
        返回:
            dict: 信号信息字典 {'sinr': 值，'rsrp': 值}
        """
        result = {'sinr': 0, 'rsrp': 0}
        sig_list = net.getSignal(1)
        
        for item in sig_list:
            if len(item) == 5 and item[0] != 99:
                result = {
                    'sinr': item[3],
                    'rsrp': item[1]
                }
                break
        
        return result
    
    def get_cell_id(self):
        """
        获取小区 ID
        
        返回:
            int: 小区 ID
        """
        cell_list = net.getCellInfo()
        for item in cell_list:
            if len(item) > 0:
                for real_item in item:
                    if len(real_item) > 0:
                        return real_item[1]
        return 0
    
    def get_network_info(self):
        """
        获取完整网络信息
        
        返回:
            dict: 网络信息字典
        """
        if not self.wait_connected(30):
            return None
        
        # 同步时间
        self.sync_time()
        
        sig_info = self.get_signal_info()
        
        self.net_info = {
            'signal_power': net.csqQueryPoll(),
            'cell_id': self.get_cell_id(),
            'ecl': net.csqQueryPoll(),
            'pci': net.getServingCi(),
            'sinr': sig_info['sinr'],
            'rsrp': sig_info['rsrp'],
            'IMEI': modem.getDevImei(),
            'IMSI': sim.getImsi(),
            'ccid': sim.getIccid()
        }
        
        return self.net_info
    
    def is_connected(self):
        """
        检查网络是否连接
        
        返回:
            bool: 连接状态
        """
        stage, state = self.checknet.wait_network_connected(5)
        sim_status = sim.getStatus()
        return stage == 3 and state == 1 and sim_status == 1
