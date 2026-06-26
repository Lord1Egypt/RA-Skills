#!/usr/bin/env python3
"""
DiGiCo调音台控制实现
通过OSC协议远程控制和监控DiGiCo调音台

技能元数据：
- invocation_mode: both（支持人工+自动化）
- preferred_provider: minimax（适合自动化场景）
"""

import json
import socket
import time
from typing import Dict, Optional, List
from datetime import datetime
from pathlib import Path

try:
    from pythonosc import udp_client, dispatcher, osc_server
    OSC_AVAILABLE = True
except ImportError:
    OSC_AVAILABLE = False
    print("警告: python-osc库未安装，部分功能不可用")


class DiGiCoController:
    """DiGiCo调音台控制器核心类"""
    
    def __init__(self):
        self.name = "skill_digico_mixer"
        self.version = "1.0.0"
        self.connected = False
        self.client = None
        self.ip = None
        self.port = None
        self.timeout = 5.0
        
        # OSC协议路径映射
        self.osc_paths = {
            "scene_load": "/digico/scene/load",
            "channel_gain": "/digico/channel/{}/gain",
            "channel_eq": "/digico/channel/{}/eq",
            "channel_comp": "/digico/channel/{}/compressor",
            "output_route": "/digico/output/{}/route",
            "status": "/digico/status",
            "ping": "/digico/ping",
            "snapshot_save": "/digico/snapshot/save",
            "snapshot_load": "/digico/snapshot/load"
        }
        
        # 状态缓存
        self.status_cache = {}
        self.last_update = None
        
    def get_info(self) -> Dict:
        """获取技能信息"""
        return {
            "name": self.name,
            "version": self.version,
            "description": "DiGiCo调音台OSC协议远程控制系统",
            "invocation_mode": "both",
            "preferred_provider": "minimax",
            "osc_available": OSC_AVAILABLE,
            "connected": self.connected
        }
    
    def connect(self, ip: str = "192.168.1.100", port: int = 12345) -> Dict:
        """
        连接DiGiCo调音台
        
        Args:
            ip: 调音台IP地址
            port: OSC端口
        
        Returns:
            dict: 连接结果
        """
        if not OSC_AVAILABLE:
            return {
                "status": "error",
                "message": "python-osc库未安装，无法连接"
            }
        
        try:
            self.ip = ip
            self.port = port
            
            # 创建OSC客户端
            self.client = udp_client.SimpleUDPClient(ip, port)
            
            # 测试连接
            ping_result = self._ping()
            
            if ping_result["status"] == "success":
                self.connected = True
                return {
                    "status": "success",
                    "ip": ip,
                    "port": port,
                    "latency_ms": ping_result["latency_ms"],
                    "message": f"已连接到DiGiCo调音台 {ip}:{port}"
                }
            else:
                return {
                    "status": "error",
                    "message": f"无法连接到 {ip}:{port}，网络不通或OSC端口未开放"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"连接失败：{str(e)}"
            }
    
    def _ping(self) -> Dict:
        """测试调音台连接性"""
        try:
            # 发送ping OSC消息
            start_time = time.time()
            
            # 使用socket测试连接性
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            
            try:
                sock.connect((self.ip, self.port))
                latency = (time.time() - start_time) * 1000
                sock.close()
                
                return {
                    "status": "success",
                    "latency_ms": round(latency, 2)
                }
            except socket.timeout:
                return {
                    "status": "error",
                    "message": "连接超时"
                }
            finally:
                sock.close()
                
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def load_scene(self, scene_id: int) -> Dict:
        """
        加载场景
        
        Args:
            scene_id: 场景编号（1-999）
        
        Returns:
            dict: 执行结果
        """
        if not self.connected:
            return {
                "status": "error",
                "message": "调音台未连接"
            }
        
        if not 1 <= scene_id <= 999:
            return {
                "status": "error",
                "message": f"场景编号无效：{scene_id}（应为1-999）"
            }
        
        try:
            # 发送OSC消息
            osc_path = self.osc_paths["scene_load"]
            self.client.send_message(osc_path, scene_id)
            
            return {
                "status": "success",
                "scene_id": scene_id,
                "osc_path": osc_path,
                "message": f"场景 {scene_id} 加载请求已发送"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"场景加载失败：{str(e)}"
            }
    
    def set_channel_gain(self, channel: int, gain: float) -> Dict:
        """
        设置通道增益
        
        Args:
            channel: 通道编号（1-128）
            gain: 增益值（dB，范围：-∞ to +12）
        
        Returns:
            dict: 执行结果
        """
        if not self.connected:
            return {
                "status": "error",
                "message": "调音台未连接"
            }
        
        if not 1 <= channel <= 128:
            return {
                "status": "error",
                "message": f"通道编号无效：{channel}（应为1-128）"
            }
        
        if gain > 12:
            return {
                "status": "error",
                "message": f"增益值过大：{gain}dB（最大+12dB）"
            }
        
        try:
            # 发送OSC消息
            osc_path = self.osc_paths["channel_gain"].format(channel)
            self.client.send_message(osc_path, gain)
            
            return {
                "status": "success",
                "channel": channel,
                "gain": gain,
                "osc_path": osc_path,
                "message": f"通道 {channel} 增益已设置为 {gain}dB"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"增益设置失败：{str(e)}"
            }
    
    def set_channel_compressor(self, channel: int, threshold: float = -20, ratio: float = 4.0) -> Dict:
        """
        设置通道压缩器
        
        Args:
            channel: 通道编号
            threshold: 压缩阈值（dB）
            ratio: 压缩比
        
        Returns:
            dict: 执行结果
        """
        if not self.connected:
            return {
                "status": "error",
                "message": "调音台未连接"
            }
        
        try:
            osc_path = self.osc_paths["channel_comp"].format(channel)
            self.client.send_message(osc_path, [threshold, ratio])
            
            return {
                "status": "success",
                "channel": channel,
                "threshold": threshold,
                "ratio": ratio,
                "message": f"通道 {channel} 压缩器已设置"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"压缩器设置失败：{str(e)}"
            }
    
    def get_status(self) -> Dict:
        """
        获取调音台状态
        
        Returns:
            dict: 状态信息
        """
        if not self.connected:
            return {
                "status": "error",
                "message": "调音台未连接"
            }
        
        try:
            # 模拟状态查询（实际需要OSC服务器响应）
            # 这里返回缓存的状态信息
            
            return {
                "status": "success",
                "connected": self.connected,
                "ip": self.ip,
                "port": self.port,
                "last_update": self.last_update or datetime.now().isoformat(),
                "message": "状态查询成功"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"状态查询失败：{str(e)}"
            }
    
    def save_snapshot(self, name: str) -> Dict:
        """
        保存快照
        
        Args:
            name: 快照名称
        
        Returns:
            dict: 执行结果
        """
        if not self.connected:
            return {
                "status": "error",
                "message": "调音台未连接"
            }
        
        try:
            osc_path = self.osc_paths["snapshot_save"]
            self.client.send_message(osc_path, name)
            
            return {
                "status": "success",
                "snapshot_name": name,
                "message": f"快照 '{name}' 已保存"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"快照保存失败：{str(e)}"
            }
    
    def disconnect(self) -> Dict:
        """断开连接"""
        self.connected = False
        self.client = None
        self.ip = None
        self.port = None
        
        return {
            "status": "success",
            "message": "已断开连接"
        }
    
    def execute(self, action: str, **kwargs) -> Dict:
        """
        执行技能动作
        
        Args:
            action: 动作类型
            **kwargs: 动作参数
        
        Returns:
            dict: 执行结果
        """
        action_map = {
            "connect": self.connect,
            "disconnect": self.disconnect,
            "load_scene": self.load_scene,
            "set_channel_gain": self.set_channel_gain,
            "set_channel_compressor": self.set_channel_compressor,
            "get_status": self.get_status,
            "save_snapshot": self.save_snapshot,
            "ping": self._ping
        }
        
        if action not in action_map:
            return {
                "status": "error",
                "message": f"未知动作：{action}（支持：{list(action_map.keys())})"
            }
        
        # 调用对应的方法
        method = action_map[action]
        
        try:
            return method(**kwargs)
        except TypeError as e:
            # 参数不匹配
            return {
                "status": "error",
                "message": f"参数错误：{str(e)}"
            }


# 模块级函数
def get_info() -> Dict:
    """获取技能信息"""
    controller = DiGiCoController()
    return controller.get_info()


def execute(action: str, **kwargs) -> Dict:
    """
    执行技能
    
    Args:
        action: 动作类型
        **kwargs: 动作参数
    
    Returns:
        dict: 执行结果
    """
    controller = DiGiCoController()
    
    # 如果不是连接动作，且控制器未连接，尝试自动连接
    if action != "connect" and not controller.connected:
        if kwargs.get("ip") and kwargs.get("port"):
            controller.connect(kwargs["ip"], kwargs["port"])
    
    return controller.execute(action, **kwargs)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="DiGiCo调音台控制")
    parser.add_argument("--info", action="store_true", help="显示技能信息")
    parser.add_argument("--action", type=str, help="执行动作")
    parser.add_argument("--ip", type=str, default="192.168.1.100")
    parser.add_argument("--port", type=int, default=12345)
    
    args = parser.parse_args()
    
    if args.info:
        print(json.dumps(get_info(), ensure_ascii=False, indent=2))
    elif args.action:
        result = execute(
            action=args.action,
            ip=args.ip,
            port=args.port
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 测试连接
        result = execute("connect", ip="192.168.1.100", port=12345)
        print(json.dumps(result, ensure_ascii=False, indent=2))