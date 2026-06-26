#!/usr/bin/env python3
"""
push_helper.py - 统一推送助手

根据条件自动选择推送渠道：
- MeoW：用户拥有 HarmonyOS 设备 + 启用 MeoW + 配置昵称
- 负一屏：默认启用
- 双渠道：两者都启用时同时推送
"""

import json
import sys
from pathlib import Path
from typing import Optional

# 尝试导入 feature_flag
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from feature_flag import FeatureFlag
    _ff = FeatureFlag()
except:
    _ff = None

# MeoW 推送脚本路径
MEOW_SCRIPT = Path(__file__).parent.parent.parent / "today-task" / "scripts" / "meow_pusher.py"

class PushHelper:
    """统一推送助手"""
    
    def __init__(self):
        self.ff = _ff
    
    def _get_flag(self, key: str, default=None):
        """获取 feature flag"""
        if self.ff:
            try:
                val = self.ff.get(key)
                return val if val is not None else default
            except:
                return default
        return default
    
    def should_use_meow(self) -> bool:
        """检查是否应该使用 MeoW"""
        # 必须满足：1. HarmonyOS设备 2. MeoW启用 3. 有昵称
        has_harmonyos = self._get_flag("push.harmonyos_device", False)
        meow_enabled = self._get_flag("push.meow_enabled", False)
        nickname = self._get_flag("push.meow_nickname", "")
        
        return has_harmonyos and meow_enabled and bool(nickname)
    
    def should_use_today_task(self) -> bool:
        """检查是否应该使用负一屏"""
        return True  # 负一屏默认启用
    
    def push(self, task_name: str, content: str, result: str = "完成") -> dict:
        """
        统一推送接口
        
        返回:
        {
            "success": bool,
            "today_task": {...},  # 负一屏结果
            "meow": {...},        # MeoW结果（如果有）
            "channels_used": ["today_task", "meow"]
        }
        """
        results = {
            "success": False,
            "today_task": None,
            "meow": None,
            "channels_used": []
        }
        
        # 负一屏推送
        if self.should_use_today_task():
            tt_result = self._push_today_task(task_name, content, result)
            results["today_task"] = tt_result
            results["channels_used"].append("today_task")
        
        # MeoW 推送
        if self.should_use_meow():
            meow_result = self._push_meow(task_name, content, result)
            results["meow"] = meow_result
            results["channels_used"].append("meow")
        
        # 判断成功
        if results["today_task"] and results["today_task"].get("success"):
            results["success"] = True
        if results["meow"] and results["meow"].get("success"):
            results["success"] = True
        
        return results
    
    def _push_today_task(self, task_name: str, content: str, result: str) -> dict:
        """推送负一屏"""
        try:
            # today-task/scripts 与 yaoyao-memory 平级
            today_task_path = Path(__file__).parent.parent.parent / "today-task" / "scripts"
            sys.path.insert(0, str(today_task_path))
            from quick_push import push as qt_push
            return qt_push(task_name, content, result)
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _push_meow(self, task_name: str, content: str, result: str) -> dict:
        """推送 MeoW"""
        try:
            nickname = self._get_flag("push.meow_nickname", "")
            if not nickname:
                return {"success": False, "error": "未配置 MeoW 昵称"}
            
            # 动态导入
            import importlib.util
            spec = importlib.util.spec_from_file_location("meow_pusher", MEOW_SCRIPT)
            if not spec or not spec.loader:
                return {"success": False, "error": "MeoW 脚本不存在"}
            
            meow_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(meow_module)
            
            # 使用 POST 格式
            return meow_module.push_post(nickname, task_name, f"{content}\n\n{result}")
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def enable_meow(self, nickname: str):
        """启用 MeoW"""
        if self.ff:
            self.ff.set("push.meow_enabled", True)
            self.ff.set("push.meow_nickname", nickname)
            return True
        return False
    
    def disable_meow(self):
        """禁用 MeoW"""
        if self.ff:
            self.ff.set("push.meow_enabled", False)
            return True
        return False
    
    def set_harmonyos(self, has_harmonyos: bool):
        """设置 HarmonyOS 设备状态"""
        if self.ff:
            self.ff.set("push.harmonyos_device", has_harmonyos)
            return True
        return False
    
    def status(self) -> dict:
        """获取推送状态"""
        return {
            "today_task": self.should_use_today_task(),
            "meow": self.should_use_meow(),
            "meow_configured": bool(self._get_flag("push.meow_nickname", "")),
            "harmonyos": self._get_flag("push.harmonyos_device", False),
        }


if __name__ == "__main__":
    helper = PushHelper()
    
    print("📤 推送状态:")
    status = helper.status()
    for k, v in status.items():
        print(f"  {k}: {v}")
    
    print("\n🧪 测试推送:")
    result = helper.push("测试任务", "# 测试内容", "测试结果")
    print(f"成功: {result['success']}")
    print(f"渠道: {result['channels_used']}")
    print(f"负一屏: {result['today_task']}")
    print(f"MeoW: {result['meow']}")
