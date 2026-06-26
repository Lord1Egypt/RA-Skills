#!/usr/bin/env python3
"""
feature_flag.py - Feature Flag 管理系统

参考 Claude Code 的 Feature Flag 体系，支持：
- 差异化功能控制
- A/B 测试支持
- 灰度发布
- 配置继承

用法：
    python3 feature_flag.py list                    # 列出所有开关
    python3 feature_flag.py get <flag>            # 获取开关状态
    python3 feature_flag.py enable <flag>         # 启用开关
    python3 feature_flag.py disable <flag>        # 禁用开关
    python3 feature_flag.py set <flag> <value>    # 设置值
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Optional

# Feature Flag 存储路径
FLAG_DIR = Path.home() / ".openclaw" / "features"
FLAG_FILE = FLAG_DIR / "flags.json"
FLAG_CONFIG = FLAG_DIR / "config.json"

# 内置 Feature Flag 定义
BUILTIN_FLAGS = {
    # === 记忆系统 (Memory) ===
    "memory.silent_mode": {
        "type": "bool",
        "default": False,
        "description": "静默模式（记录前无需确认）",
        "tags": ["memory", "ux"],
    },
    "memory.auto_promote": {
        "type": "bool",
        "default": True,
        "description": "自动升级记忆到更高层级",
        "tags": ["memory", "auto"],
    },
    "memory.auto_cleanup": {
        "type": "bool",
        "default": True,
        "description": "自动清理过期记忆",
        "tags": ["memory", "auto"],
    },
    "memory.summarize_daily": {
        "type": "bool",
        "default": True,
        "description": "每日自动生成摘要",
        "tags": ["memory", "auto"],
    },
    "memory.vector_search": {
        "type": "bool",
        "default": True,
        "description": "启用向量搜索增强",
        "tags": ["memory", "search"],
    },
    "memory.llm_enhance": {
        "type": "bool",
        "default": False,
        "description": "使用 LLM 增强记忆（需要 API Key）",
        "tags": ["memory", "llm"],
    },
    "memory.ima_sync": {
        "type": "bool",
        "default": True,
        "description": "同步到 IMA 云端",
        "tags": ["memory", "cloud"],
    },
    
    # === 搜索系统 (Search) ===
    "search.hybrid": {
        "type": "bool",
        "default": True,
        "description": "混合搜索（向量 + 关键词）",
        "tags": ["search", "vector"],
    },
    "search.query_rewrite": {
        "type": "bool",
        "default": True,
        "description": "查询改写优化",
        "tags": ["search", "llm"],
    },
    "search.fuzzy": {
        "type": "bool",
        "default": True,
        "description": "模糊匹配",
        "tags": ["search"],
    },
    "search.cache": {
        "type": "bool",
        "default": True,
        "description": "搜索结果缓存",
        "tags": ["search", "cache"],
    },
    
    # === Shell 嵌入 (Shell) ===
    "shell.enabled": {
        "type": "bool",
        "default": True,
        "description": "启用 Shell 命令嵌入",
        "tags": ["shell", "experimental"],
    },
    "shell.whitelist_only": {
        "type": "bool",
        "default": True,
        "description": "仅允许白名单命令",
        "tags": ["shell", "security"],
    },
    "shell.timeout": {
        "type": "int",
        "default": 10,
        "description": "命令超时时间（秒）",
        "tags": ["shell"],
    },
    
    # === 反馈学习 (Feedback) ===
    "feedback.enabled": {
        "type": "bool",
        "default": True,
        "description": "启用反馈学习",
        "tags": ["feedback", "ml"],
    },
    "feedback.auto_adjust": {
        "type": "bool",
        "default": True,
        "description": "根据反馈自动调整参数",
        "tags": ["feedback", "auto"],
    },
    
    # === 用户体验 (UX) ===
    "ux.silent_mode": {
        "type": "bool",
        "default": True,
        "description": "静默模式（不主动提示）",
        "tags": ["ux", "silent"],
    },
    "ux.show_confidence": {
        "type": "bool",
        "default": False,
        "description": "显示答案置信度",
        "tags": ["ux"],
    },
    "ux.detailed_errors": {
        "type": "bool",
        "default": True,
        "description": "显示详细错误信息",
        "tags": ["ux", "debug"],
    },
    
    # === 实验性功能 (Experimental) ===
    "exp.smart_routing": {
        "type": "bool",
        "default": False,
        "description": "智能路由（根据查询类型选择策略）",
        "tags": ["exp", "router"],
    },
    "exp.progressive_enable": {
        "type": "bool",
        "default": True,
        "description": "渐进式功能启用",
        "tags": ["exp", "progressive"],
    },
    "exp.persona_update": {
        "type": "bool",
        "default": True,
        "description": "自动更新用户画像",
        "tags": ["exp", "persona"],
    },
    
    # === A/B 测试 ===
    "ab.test_search_v2": {
        "type": "float",
        "default": 0.0,
        "description": "搜索 v2 实验组比例（0.0-1.0）",
        "tags": ["ab", "search"],
    },
    "ab.test_memory_v2": {
        "type": "float",
        "default": 0.0,
        "description": "记忆 v2 实验组比例（0.0-1.0）",
        "tags": ["ab", "memory"],
    },
    
    # === 推送系统 (Push) ===
    "push.meow_enabled": {
        "type": "bool",
        "default": False,
        "description": "启用 MeoW 推送渠道",
        "tags": ["push", "meow"],
    },
    "push.harmonyos_device": {
        "type": "bool",
        "default": False,
        "description": "是否拥有 HarmonyOS 设备",
        "tags": ["push", "device"],
    },
    "push.dual_channel": {
        "type": "bool",
        "default": True,
        "description": "双渠道推送（负一屏 + MeoW）",
        "tags": ["push", "channel"],
    },
    "push.meow_nickname": {
        "type": "string",
        "default": "",
        "description": "MeoW 推送昵称",
        "tags": ["push", "meow"],
    },
    
    # === 自动更新 (Auto Update) ===
    "auto_update.enabled": {
        "type": "bool",
        "default": True,
        "description": "启用自动更新检查",
        "tags": ["update", "auto"],
    },
    "auto_update.check_interval": {
        "type": "int",
        "default": 3600,
        "description": "检查间隔（秒）",
        "tags": ["update", "auto"],
    },
    "auto_update.auto_install": {
        "type": "bool",
        "default": False,
        "description": "自动安装更新（需确认）",
        "tags": ["update", "auto"],
    },
}


class FeatureFlag:
    """Feature Flag 管理类"""
    
    def __init__(self):
        self.flags = {}
        self.builtin = BUILTIN_FLAGS.copy()
        self._load()
    
    def _load(self):
        """加载标志配置"""
        # 创建目录
        FLAG_DIR.mkdir(parents=True, exist_ok=True)
        
        # 加载用户配置
        if FLAG_FILE.exists():
            try:
                with open(FLAG_FILE, 'r', encoding='utf-8') as f:
                    self.flags = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.flags = {}
        
        # 合并内置默认值（不覆盖用户设置）
        for name, spec in self.builtin.items():
            if name not in self.flags:
                self.flags[name] = {"value": spec["default"]}
    
    def _save(self):
        """保存标志配置"""
        FLAG_DIR.mkdir(parents=True, exist_ok=True)
        with open(FLAG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.flags, f, indent=2, ensure_ascii=False)
    
    def get(self, name: str) -> Any:
        """获取标志值"""
        if name in self.flags:
            return self.flags[name].get("value")
        if name in self.builtin:
            return self.builtin[name]["default"]
        return None
    
    def set(self, name: str, value: Any) -> bool:
        """设置标志值"""
        # 类型检查
        if name in self.builtin:
            spec = self.builtin[name]
            expected_type = spec["type"]
            
            if expected_type == "bool" and not isinstance(value, bool):
                value = bool(value)
            elif expected_type == "int" and not isinstance(value, int):
                value = int(value)
            elif expected_type == "float" and not isinstance(value, (int, float)):
                value = float(value)
        
        self.flags[name] = {"value": value}
        self._save()
        return True
    
    def enable(self, name: str) -> bool:
        """启用标志"""
        return self.set(name, True)
    
    def disable(self, name: str) -> bool:
        """禁用标志"""
        return self.set(name, False)
    
    def list(self, tag: Optional[str] = None) -> dict:
        """列出所有标志"""
        result = {}
        for name, spec in self.builtin.items():
            value = self.get(name)
            tags = spec.get("tags", [])
            
            if tag is None or tag in tags:
                result[name] = {
                    "value": value,
                    "default": spec["default"],
                    "description": spec["description"],
                    "type": spec["type"],
                    "tags": tags,
                }
        return result
    
    def is_enabled(self, name: str) -> bool:
        """检查标志是否启用"""
        return bool(self.get(name))
    
    def in_ab_test(self, test_name: str, user_id: str = "default") -> bool:
        """检查用户是否在 A/B 测试组"""
        ratio = self.get(test_name)
        if not ratio or ratio <= 0:
            return False
        
        # 简单的哈希分配
        hash_val = hash(f"{test_name}:{user_id}")
        return (hash_val % 100) / 100.0 < ratio


def cmd_list(ff: FeatureFlag, args: list):
    """列出所有标志"""
    tag = args[0] if args else None
    flags = ff.list(tag)
    
    print(f"\n{'='*60}")
    print(f" Feature Flags ({len(flags)} flags)")
    print(f"{'='*60}")
    
    for name in sorted(flags.keys()):
        info = flags[name]
        status = "✅" if info["value"] else "❌"
        default = " (default)" if info["value"] == info["default"] else ""
        print(f"  {status} {name}")
        print(f"     └─ {info['description']}")
        print(f"       Type: {info['type']}, Value: {info['value']}{default}")
    
    print()


def cmd_get(ff: FeatureFlag, args: list):
    """获取标志值"""
    if not args:
        print("Usage: feature_flag.py get <flag>")
        return
    
    name = args[0]
    value = ff.get(name)
    
    if name in ff.builtin:
        spec = ff.builtin[name]
        print(f"\n{name}: {value}")
        print(f"  Type: {spec['type']}")
        print(f"  Default: {spec['default']}")
        print(f"  Description: {spec['description']}")
    else:
        print(f"\n{name}: {value} (unknown flag)")


def cmd_enable(ff: FeatureFlag, args: list):
    """启用标志"""
    if not args:
        print("Usage: feature_flag.py enable <flag>")
        return
    
    name = args[0]
    ff.enable(name)
    print(f"✅ Enabled: {name}")


def cmd_disable(ff: FeatureFlag, args: list):
    """禁用标志"""
    if not args:
        print("Usage: feature_flag.py disable <flag>")
        return
    
    name = args[0]
    ff.disable(name)
    print(f"❌ Disabled: {name}")


def cmd_set(ff: FeatureFlag, args: list):
    """设置标志值"""
    if len(args) < 2:
        print("Usage: feature_flag.py set <flag> <value>")
        return
    
    name, value = args[0], args[1]
    
    # 推断类型
    if value.lower() == "true":
        value = True
    elif value.lower() == "false":
        value = False
    elif value.isdigit():
        value = int(value)
    elif "." in value and value.replace(".", "").isdigit():
        value = float(value)
    
    ff.set(name, value)
    print(f"✅ Set {name} = {value}")


def cmd_check(ff: FeatureFlag, args: list):
    """检查标志状态"""
    if not args:
        print("Usage: feature_flag.py check <flag>")
        return
    
    name = args[0]
    enabled = ff.is_enabled(name)
    status = "✅ ON" if enabled else "❌ OFF"
    print(f"{name}: {status}")


def main():
    if len(sys.argv) < 2:
        print("Usage: feature_flag.py <command> [args]")
        print("\nCommands:")
        print("  list [tag]      - 列出所有标志（可选：按标签过滤）")
        print("  get <flag>      - 获取标志值")
        print("  enable <flag>  - 启用标志")
        print("  disable <flag> - 禁用标志")
        print("  set <flag> <v> - 设置值")
        print("  check <flag>   - 检查是否启用")
        sys.exit(1)
    
    ff = FeatureFlag()
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    commands = {
        "list": cmd_list,
        "get": cmd_get,
        "enable": cmd_enable,
        "disable": cmd_disable,
        "set": cmd_set,
        "check": cmd_check,
    }
    
    if cmd in commands:
        commands[cmd](ff, args)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
