#!/usr/bin/env python3
"""
配置面板 - 用户友好的配置管理工具
用法: python3 scripts/config_panel.py [命令] [参数]
"""

import sys
import os
from pathlib import Path

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
os.chdir(str(script_dir))

from feature_flag import FeatureFlag


class ConfigPanel:
    """配置面板"""
    
    def __init__(self):
        self.ff = FeatureFlag()
        self.builtin = self.ff.builtin
        
    def list_all(self) -> str:
        """列出所有配置"""
        # 分组
        groups = {}
        for key in self.builtin:
            parts = key.split('.')
            group = parts[0] if parts else 'other'
            if group not in groups:
                groups[group] = []
            groups[group].append(key)
        
        lines = ["```", "📋 配置文件面板", "=" * 40, ""]
        
        for group in sorted(groups.keys()):
            lines.append(f"\n【{group.upper()}】")
            for key in sorted(groups[group]):
                val = self.ff.get(key)
                val_str = "开" if val is True else "关" if val is False else str(val)
                lines.append(f"  {key}: {val_str}")
        
        lines.append("\n```")
        return "\n".join(lines)
    
    def get(self, key: str) -> str:
        """获取单个配置"""
        if key not in self.builtin:
            return f"❌ 未知配置: {key}"
        
        val = self.ff.get(key)
        return f"📌 {key} = {val}"
    
    def set(self, key: str, value) -> str:
        """设置配置"""
        if key not in self.builtin:
            return f"❌ 未知配置: {key}"
        
        # 类型转换
        orig_value = value
        if value.lower() in ('true', '1', 'on', 'yes'):
            value = True
        elif value.lower() in ('false', '0', 'off', 'no'):
            value = False
        elif value.isdigit():
            value = int(value)
        
        self.ff.set(key, value)
        return f"✅ 已设置: {key} = {orig_value}"
    
    def enable(self, key: str) -> str:
        """启用配置"""
        return self.set(key, "true")
    
    def disable(self, key: str) -> str:
        """禁用配置"""
        return self.set(key, "false")
    
    def toggle(self, key: str) -> str:
        """切换配置"""
        if key not in self.builtin:
            return f"❌ 未知配置: {key}"
        
        val = self.ff.get(key)
        if isinstance(val, bool):
            new_val = not val
            self.ff.set(key, new_val)
            return f"✅ 已切换: {key} = {new_val}"
        else:
            return f"⚠️ {key} 不是布尔值，无法切换"
    
    def search(self, keyword: str) -> str:
        """搜索配置"""
        keyword = keyword.lower()
        matches = [k for k in self.builtin if keyword in k.lower()]
        
        if not matches:
            return f"❌ 没有找到包含 '{keyword}' 的配置"
        
        lines = [f"🔍 搜索 '{keyword}' 的结果:", ""]
        for key in sorted(matches):
            val = self.ff.get(key)
            lines.append(f"  {key}: {val}")
        
        return "\n".join(lines)
    
    def export(self) -> str:
        """导出配置"""
        lines = ["```json", "{", ]
        for key in sorted(self.builtin):
            val = self.ff.get(key)
            if isinstance(val, bool):
                val_str = "true" if val else "false"
            elif isinstance(val, str):
                val_str = f'"{val}"'
            else:
                val_str = str(val)
            lines.append(f'  "{key}": {val_str},')
        lines.append("}")
        lines.append("```")
        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(ConfigPanel().list_all())
        return
    
    cmd = sys.argv[1].lower()
    panel = ConfigPanel()
    
    if cmd == 'list':
        print(panel.list_all())
    
    elif cmd == 'get' and len(sys.argv) >= 3:
        print(panel.get(sys.argv[2]))
    
    elif cmd == 'set' and len(sys.argv) >= 4:
        print(panel.set(sys.argv[2], sys.argv[3]))
    
    elif cmd == 'enable' and len(sys.argv) >= 3:
        print(panel.enable(sys.argv[2]))
    
    elif cmd == 'disable' and len(sys.argv) >= 3:
        print(panel.disable(sys.argv[2]))
    
    elif cmd == 'toggle' and len(sys.argv) >= 3:
        print(panel.toggle(sys.argv[2]))
    
    elif cmd == 'search' and len(sys.argv) >= 3:
        print(panel.search(sys.argv[2]))
    
    elif cmd == 'export':
        print(panel.export())
    
    else:
        print("""📋 配置面板命令:

```bash
# 列出所有配置
python3 scripts/config_panel.py list

# 获取单个配置
python3 scripts/config_panel.py get memory.auto_cleanup

# 设置配置
python3 scripts/config_panel.py set memory.auto_cleanup false
python3 scripts/config_panel.py set shell.timeout 30

# 启用/禁用
python3 scripts/config_panel.py enable memory.auto_cleanup
python3 scripts/config_panel.py disable memory.auto_cleanup

# 切换配置
python3 scripts/config_panel.py toggle ux.silent_mode

# 搜索配置
python3 scripts/config_panel.py search memory

# 导出配置
python3 scripts/config_panel.py export
```
""")


if __name__ == '__main__':
    main()
