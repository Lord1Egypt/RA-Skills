#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ivr_engine.py — 多级 IVR 菜单引擎（v2.6）

功能：
1. 加载 menu.yaml 多级菜单配置
2. 支持说数字或说名称双选择方式
3. 0 重复听、9 转人工、8 返回上级
4. 超时/重试/非法输入处理
5. 菜单结构完全 YAML 配置化

依赖：纯 Python 标准库（yaml 可选，不可用时降级为 json）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-08-24)
"""

import os
import re
import json
import logging
from typing import Optional, Dict, List, Any

logger = logging.getLogger(__name__)

# 尝试导入 pyyaml，不可用时降级为 json
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


# ==========================================
# 配置
# ==========================================

CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config')
MENU_FILE_YAML = os.path.join(CONFIG_DIR, 'menu.yaml')
MENU_FILE_JSON = os.path.join(CONFIG_DIR, 'menu.json')


# ==========================================
# IVR 菜单引擎
# ==========================================

class IVREngine:
    """
    多级 IVR 菜单引擎
    
    支持：
    - 说数字或说名称双选择
    - 0 重复听当前菜单
    - 9 转人工客服
    - 8 返回上级菜单
    - 超时自动重复
    - 非法输入重试
    
    使用方式：
        engine = IVREngine()
        engine.load()
        
        # 获取根菜单欢迎语
        welcome = engine.get_welcome_text()
        
        # 处理用户输入
        result = engine.process_input("1")
        # result: {"action": "submenu", "target": "sales_menu", "text": "..."}
    """

    def __init__(self, config_path: str = None):
        """
        初始化 IVR 引擎
        
        Args:
            config_path: 菜单配置文件路径，None 则使用默认路径
        """
        self.config_path = config_path
        self.menu_config: Dict = {}
        self._current_menu: str = "root"
        self._menu_stack: List[str] = []  # 菜单栈，用于返回上级
        self._retry_count: int = 0
        self._max_retries: int = 3
        self._loaded = False
        
    def load(self) -> bool:
        """
        加载菜单配置文件
        
        Returns:
            bool: 加载成功返回 True
        """
        # 确定配置文件路径
        if self.config_path:
            path = self.config_path
        elif YAML_AVAILABLE and os.path.exists(MENU_FILE_YAML):
            path = MENU_FILE_YAML
        elif os.path.exists(MENU_FILE_JSON):
            path = MENU_FILE_JSON
        elif os.path.exists(MENU_FILE_YAML):
            path = MENU_FILE_YAML
        else:
            logger.error(f"菜单配置文件不存在: {MENU_FILE_YAML}")
            return False
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                if path.endswith('.yaml') or path.endswith('.yml'):
                    if YAML_AVAILABLE:
                        self.menu_config = yaml.safe_load(f)
                    else:
                        self.menu_config = json.load(f)
                else:
                    self.menu_config = json.load(f)
            
            if not self.menu_config:
                logger.error("菜单配置文件为空")
                return False
            
            self._loaded = True
            self._max_retries = self.menu_config.get('settings', {}).get('input', {}).get('max_retries', 3)
            logger.info(f"IVR 菜单加载完成")
            return True
            
        except Exception as e:
            logger.error(f"加载菜单配置文件失败: {e}")
            return False
    
    def get_welcome_text(self) -> str:
        """获取根菜单欢迎语"""
        if not self._loaded:
            return "您好，欢迎致电。"
        root = self.menu_config.get('root', {})
        return root.get('welcome_text', '您好，欢迎致电。')
    
    def get_menu_text(self, menu_name: str = None) -> str:
        """
        获取指定菜单的完整播报文本
        
        Args:
            menu_name: 菜单名称，None 则使用当前菜单
            
        Returns:
            str: 完整播报文本
        """
        if not self._loaded:
            return "菜单加载失败。"
        
        menu_name = menu_name or self._current_menu
        
        if menu_name == "root":
            menu = self.menu_config.get('root', {})
        else:
            menu = self.menu_config.get(menu_name, {})
        
        if not menu:
            return "菜单不存在。"
        
        # 构建播报文本
        lines = []
        
        # 菜单标题/介绍
        title = menu.get('title', '')
        intro = menu.get('intro_text', '')
        if title and menu_name != "root":
            lines.append(f"{title}。")
        if intro:
            lines.append(intro)
        
        # 菜单项
        items = menu.get('menu_items', [])
        for item in items:
            key = item.get('key', '')
            name = item.get('name', '')
            lines.append(f"按 {key}，{name}。")
        
        # 全局选项
        lines.append("按 0，重复收听。")
        lines.append("按 9，转人工服务。")
        
        if menu_name != "root":
            lines.append("按 8，返回上级。")
        
        return "\n".join(lines)
    
    def process_input(self, user_input: str, menu_name: str = None) -> Dict[str, Any]:
        """
        处理用户输入
        
        Args:
            user_input: 用户输入（数字或名称）
            menu_name: 当前菜单名称，None 则使用当前菜单
            
        Returns:
            dict: {
                "action": "submenu" | "intent" | "transfer_human" | "repeat" | "back" | "invalid",
                "target": "目标菜单/意图",
                "text": "播报文本",
                "handled": bool
            }
        """
        if not self._loaded:
            return {"action": "error", "text": "系统错误，请稍后再试。", "handled": False}
        
        menu_name = menu_name or self._current_menu
        user_input = user_input.strip()
        
        if not user_input:
            return self._handle_invalid("输入为空")
        
        # 获取当前菜单配置
        if menu_name == "root":
            menu = self.menu_config.get('root', {})
        else:
            menu = self.menu_config.get(menu_name, {})
        
        if not menu:
            return self._handle_invalid("菜单不存在")
        
        items = menu.get('menu_items', [])
        
        # 特殊按键处理
        if user_input == "0":
            return self._handle_repeat(menu_name)
        
        if user_input == "9":
            return self._handle_transfer_human()
        
        if user_input == "8" and menu_name != "root":
            return self._handle_back()
        
        # 匹配菜单项（数字或名称）
        matched_item = self._match_item(user_input, items)
        
        if matched_item:
            self._retry_count = 0  # 重置重试计数
            return self._handle_item(matched_item, menu_name)
        
        # 未匹配到，处理非法输入
        return self._handle_invalid(user_input)
    
    def navigate_to(self, menu_name: str):
        """
        导航到指定菜单
        
        Args:
            menu_name: 目标菜单名称
        """
        self._menu_stack.append(self._current_menu)
        self._current_menu = menu_name
        self._retry_count = 0
    
    def go_back(self) -> str:
        """
        返回上级菜单
        
        Returns:
            str: 上级菜单名称
        """
        if self._menu_stack:
            self._current_menu = self._menu_stack.pop()
        else:
            self._current_menu = "root"
        self._retry_count = 0
        return self._current_menu
    
    def reset(self):
        """重置到根菜单"""
        self._current_menu = "root"
        self._menu_stack = []
        self._retry_count = 0
    
    def get_current_menu(self) -> str:
        """获取当前菜单名称"""
        return self._current_menu

    # === 内部处理方法 ===

    def _match_item(self, user_input: str, items: List[Dict]) -> Optional[Dict]:
        """
        匹配菜单项（支持数字和名称）
        
        Args:
            user_input: 用户输入
            items: 菜单项列表
            
        Returns:
            dict or None: 匹配到的菜单项
        """
        user_input_lower = user_input.lower().strip()
        
        for item in items:
            # 数字匹配
            if user_input == item.get('key', ''):
                return item
            
            # 名称匹配（模糊匹配）
            name = item.get('name', '')
            display_name = item.get('display_name', name)
            
            # 完全匹配
            if user_input_lower == name.lower() or user_input_lower == display_name.lower():
                return item
            
            # 包含匹配（如用户说"销售"匹配"销售咨询"）
            if len(user_input) >= 2:
                if user_input in name or user_input in display_name:
                    return item
        
        return None

    def _handle_item(self, item: Dict, current_menu: str) -> Dict[str, Any]:
        """处理菜单项选择"""
        action = item.get('action', '')
        target = item.get('target', '')
        name = item.get('name', '')
        
        if action == "submenu":
            # 进入子菜单
            self.navigate_to(target)
            return {
                "action": "submenu",
                "target": target,
                "text": self.get_menu_text(target),
                "handled": True,
            }
        elif action == "intent":
            # 触发意图
            return {
                "action": "intent",
                "target": target,
                "text": f"正在为您转接{name}。",
                "handled": True,
            }
        elif action == "transfer_human":
            return self._handle_transfer_human()
        elif action == "back":
            return self._handle_back()
        else:
            return self._handle_invalid(f"未知操作: {action}")

    def _handle_repeat(self, menu_name: str) -> Dict[str, Any]:
        """处理重复听"""
        root = self.menu_config.get('root', {})
        repeat_text = root.get('repeat_text', '重新为您播报菜单。')
        
        return {
            "action": "repeat",
            "target": menu_name,
            "text": repeat_text + "\n" + self.get_menu_text(menu_name),
            "handled": True,
        }

    def _handle_transfer_human(self) -> Dict[str, Any]:
        """处理转人工"""
        return {
            "action": "transfer_human",
            "target": "",
            "text": "正在为您转接人工客服，请稍等。",
            "handled": True,
        }

    def _handle_back(self) -> Dict[str, Any]:
        """处理返回上级"""
        parent = self.go_back()
        return {
            "action": "back",
            "target": parent,
            "text": self.get_menu_text(parent),
            "handled": True,
        }

    def _handle_invalid(self, user_input: str) -> Dict[str, Any]:
        """处理非法输入"""
        self._retry_count += 1
        
        root = self.menu_config.get('root', {})
        
        if self._retry_count >= self._max_retries:
            # 超过最大重试次数，转人工
            return {
                "action": "transfer_human",
                "target": "",
                "text": "输入错误次数过多，正在为您转接人工客服。",
                "handled": True,
            }
        
        invalid_text = root.get('invalid_input_text', '输入有误，请重新选择。')
        
        return {
            "action": "invalid",
            "target": self._current_menu,
            "text": invalid_text,
            "handled": False,
            "retry_count": self._retry_count,
        }


# ==========================================
# 便捷函数
# ==========================================

def get_ivr_welcome(config_path: str = None) -> str:
    """便捷函数：获取 IVR 欢迎语"""
    engine = IVREngine(config_path)
    engine.load()
    return engine.get_welcome_text()


def process_ivr_input(user_input: str, menu_name: str = None,
                      config_path: str = None) -> Dict[str, Any]:
    """便捷函数：处理 IVR 输入"""
    engine = IVREngine(config_path)
    engine.load()
    return engine.process_input(user_input, menu_name)


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """运行 IVR 引擎自测"""
    print("=" * 60)
    print("IVR 多级菜单引擎 — 自测模式")
    print("=" * 60)
    
    engine = IVREngine()
    if not engine.load():
        print("❌ IVR 引擎加载失败")
        return
    
    # 测试 1: 欢迎语
    print("\n[测试 1] 欢迎语")
    welcome = engine.get_welcome_text()
    print(f"  欢迎语: {welcome[:50]}...")
    assert len(welcome) > 0
    print("✅ 欢迎语通过")
    
    # 测试 2: 数字选择
    print("\n[测试 2] 数字选择")
    result = engine.process_input("1")
    print(f"  输入 '1': action={result['action']}, target={result['target']}")
    assert result['action'] == 'submenu'
    assert result['target'] == 'sales_menu'
    print("✅ 数字选择通过")
    
    # 测试 3: 名称选择
    print("\n[测试 3] 名称选择")
    engine.reset()
    result = engine.process_input("销售咨询")
    print(f"  输入 '销售咨询': action={result['action']}, target={result['target']}")
    assert result['action'] == 'submenu'
    assert result['target'] == 'sales_menu'
    print("✅ 名称选择通过")
    
    # 测试 4: 子菜单导航
    print("\n[测试 4] 子菜单导航")
    result = engine.process_input("1")
    print(f"  子菜单输入 '1': action={result['action']}, target={result['target']}")
    assert result['action'] == 'intent'
    print("✅ 子菜单导航通过")
    
    # 测试 5: 重复听（0）
    print("\n[测试 5] 重复听")
    result = engine.process_input("0")
    print(f"  输入 '0': action={result['action']}")
    assert result['action'] == 'repeat'
    print("✅ 重复听通过")
    
    # 测试 6: 转人工（9）
    print("\n[测试 6] 转人工")
    result = engine.process_input("9")
    print(f"  输入 '9': action={result['action']}")
    assert result['action'] == 'transfer_human'
    print("✅ 转人工通过")
    
    # 测试 7: 返回上级（8）
    print("\n[测试 7] 返回上级")
    engine.navigate_to("sales_menu")
    result = engine.process_input("8")
    print(f"  输入 '8': action={result['action']}, target={result['target']}")
    assert result['action'] == 'back'
    print("✅ 返回上级通过")
    
    # 测试 8: 非法输入
    print("\n[测试 8] 非法输入")
    engine.reset()
    result = engine.process_input("abc")
    print(f"  输入 'abc': action={result['action']}, retry={result.get('retry_count')}")
    assert result['action'] == 'invalid'
    print("✅ 非法输入通过")
    
    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_self_test()
