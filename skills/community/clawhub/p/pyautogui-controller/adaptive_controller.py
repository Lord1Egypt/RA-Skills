#!/usr/bin/env python3
"""
自适应控制器 - 适配不同网站的智能控制
能够自动学习网站布局，适应不同页面结构
"""

import pyautogui
import time
import json
from typing import Optional, Dict, List, Tuple
from pathlib import Path

class AdaptiveController:
    """自适应控制器"""
    
    def __init__(self):
        self.width, self.height = pyautogui.size()
        self.site_configs = {}
        self.current_site = None
        self.load_configs()
    
    def load_configs(self):
        """加载网站配置"""
        config_file = Path.home() / ".pyautogui-controller" / "site_configs.json"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                self.site_configs = json.load(f)
    
    def save_configs(self):
        """保存网站配置"""
        config_dir = Path.home() / ".pyautogui-controller"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "site_configs.json"
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.site_configs, f, ensure_ascii=False, indent=2)
    
    def detect_site(self, url: str) -> str:
        """
        检测当前网站类型
        
        Args:
            url: 当前URL
        
        Returns:
            网站标识符
        """
        # 基于URL特征识别网站
        if "freegpt" in url:
            return "freegpt"
        elif "chat" in url:
            return "generic_chat"
        elif "google" in url:
            return "google"
        elif "baidu" in url:
            return "baidu"
        else:
            return "unknown"
    
    def learn_site(self, site_id: str) -> Dict:
        """
        学习新网站布局
        
        Args:
            site_id: 网站标识符
        
        Returns:
            学习到的配置
        """
        print(f"🎓 学习网站布局: {site_id}")
        
        config = {
            "site_id": site_id,
            "screen_size": (self.width, self.height),
            "elements": {}
        }
        
        # 自动探测常见元素位置
        config["elements"]["input_box"] = self._find_input_box_heuristic()
        config["elements"]["send_button"] = self._find_send_button_heuristic()
        config["elements"]["verify_checkbox"] = self._find_verify_checkbox_heuristic()
        
        # 保存配置
        self.site_configs[site_id] = config
        self.save_configs()
        
        print(f"✅ 已学习 {site_id} 布局")
        return config
    
    def _find_input_box_heuristic(self) -> Optional[Dict]:
        """
        启发式查找输入框
        
        策略：
        1. 底部区域白色长条
        2. 宽度占屏幕大部分
        3. 高度适中（30-100像素）
        """
        # 扫描底部区域
        scan_y_start = int(self.height * 0.8)
        scan_y_end = self.height - 20
        
        candidates = []
        
        for y in range(scan_y_start, scan_y_end, 10):
            # 扫描水平线
            white_segments = []
            start_x = None
            
            for x in range(100, self.width - 100, 5):
                try:
                    color = pyautogui.pixel(x, y)
                    # 检测白色或浅色区域
                    if color[0] > 240 and color[1] > 240 and color[2] > 240:
                        if start_x is None:
                            start_x = x
                    else:
                        if start_x is not None:
                            width = x - start_x
                            if width > 300:  # 足够宽
                                white_segments.append((start_x, y, width))
                            start_x = None
                except:
                    pass
            
            candidates.extend(white_segments)
        
        # 返回最可能的输入框
        if candidates:
            # 选择最宽的
            best = max(candidates, key=lambda c: c[2])
            return {
                "x": best[0] + best[2] // 2,
                "y": best[1],
                "width": best[2],
                "confidence": 0.7
            }
        
        return None
    
    def _find_send_button_heuristic(self) -> Optional[Dict]:
        """
        启发式查找发送按钮
        
        策略：
        1. 输入框附近
        2. 蓝色或绿色
        3. 圆形或圆角矩形
        """
        # 常见位置：输入框右侧或下方
        candidates = [
            (self.width - 100, self.height - 100),
            (self.width - 150, self.height - 100),
            (self.width * 3 // 4, self.height - 100),
        ]
        
        for pos in candidates:
            try:
                color = pyautogui.pixel(pos[0], pos[1])
                # 检测蓝色按钮
                if color[2] > 150 and color[0] < 100:
                    return {
                        "x": pos[0],
                        "y": pos[1],
                        "confidence": 0.6
                    }
            except:
                pass
        
        return None
    
    def _find_verify_checkbox_heuristic(self) -> Optional[Dict]:
        """
        启发式查找验证复选框
        
        策略：
        1. 屏幕中央区域
        2. 白色方形
        3. 有边框
        """
        # 常见位置：屏幕中央
        center_x = self.width // 2
        center_y = self.height // 2
        
        scan_area = [
            (center_x - 50, center_y),
            (center_x, center_y + 50),
            (center_x - 100, center_y + 100),
        ]
        
        for pos in scan_area:
            try:
                # 检测白色方形
                color = pyautogui.pixel(pos[0], pos[1])
                if color[0] > 250 and color[1] > 250 and color[2] > 250:
                    return {
                        "x": pos[0],
                        "y": pos[1],
                        "confidence": 0.5
                    }
            except:
                pass
        
        return None
    
    def get_element_position(self, element_type: str, site_id: Optional[str] = None) -> Optional[Tuple[int, int]]:
        """
        获取元素位置
        
        Args:
            element_type: 元素类型 (input_box, send_button, etc.)
            site_id: 网站标识符，None则使用当前网站
        
        Returns:
            元素坐标 (x, y)
        """
        site = site_id or self.current_site or "default"
        
        # 使用已学习的配置
        if site in self.site_configs:
            config = self.site_configs[site]
            if element_type in config.get("elements", {}):
                elem = config["elements"][element_type]
                if elem:
                    return (elem["x"], elem["y"])
        
        # 使用启发式查找
        if element_type == "input_box":
            result = self._find_input_box_heuristic()
            if result:
                return (result["x"], result["y"])
        elif element_type == "send_button":
            result = self._find_send_button_heuristic()
            if result:
                return (result["x"], result["y"])
        elif element_type == "verify_checkbox":
            result = self._find_verify_checkbox_heuristic()
            if result:
                return (result["x"], result["y"])
        
        return None
    
    def adapt_to_site(self, url: str) -> bool:
        """
        适配到指定网站
        
        Args:
            url: 网站URL
        
        Returns:
            是否成功适配
        """
        site_id = self.detect_site(url)
        self.current_site = site_id
        
        print(f"🌐 适配网站: {site_id}")
        
        # 检查是否已有配置
        if site_id in self.site_configs:
            print(f"✅ 使用已有配置")
            return True
        
        # 学习新网站
        print(f"🎓 学习新网站布局...")
        config = self.learn_site(site_id)
        
        return config is not None


class MultiSiteAutomation:
    """多网站自动化"""
    
    def __init__(self):
        self.adaptive = AdaptiveController()
        self.browser = None