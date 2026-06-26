#!/usr/bin/env python3
"""
统一配置管理器 - 一站式配置管理
整合 Feature Flags、推送设置、自动更新等所有配置
用法: python3 scripts/config_manager.py [命令] [参数]
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
os.chdir(str(script_dir))

from feature_flag import FeatureFlag


class ConfigManager:
    """统一配置管理器"""
    
    def __init__(self):
        self.ff = FeatureFlag()
        self.builtin = self.ff.builtin
        
    def dashboard(self) -> str:
        """配置仪表盘"""
        lines = [
            "```",
            "📊 yaoyao-memory 配置中心",
            "=" * 40,
            f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
        ]
        
        # 按组分类
        groups = {}
        for key in sorted(self.builtin):
            parts = key.split('.')
            group = parts[0] if parts else 'other'
            if group not in groups:
                groups[group] = []
            groups[group].append((key, self.ff.get(key)))
        
        # 统计
        total = len(self.builtin)
        enabled = sum(1 for _, v in [item for group in groups.values() for item in group] if v is True)
        disabled = sum(1 for _, v in [item for group in groups.values() for item in group] if v is False)
        
        lines.append(f"总配置数: {total}")
        lines.append(f"已启用: {enabled} | 已禁用: {disabled}")
        lines.append("")
        
        # 分类展示
        for group in sorted(groups.keys()):
            items = groups[group]
            lines.append(f"\n【{group.upper()}】({len(items)}项)")
            
            # 简化显示，只显示前5个
            for key, val in items[:5]:
                val_str = "✅" if val is True else "❌" if val is False else "📌"
                lines.append(f"  {val_str} {key}: {val}")
            
            if len(items) > 5:
                lines.append(f"  ... 还有 {len(items)-5} 项")
        
        lines.append("\n```")
        lines.append("\n💡 使用 `config_manager.py list` 查看完整列表")
        return "\n".join(lines)
    
    def list_all(self) -> str:
        """列出所有配置（详细）"""
        lines = ["```", "📋 完整配置列表", "=" * 40, ""]
        
        groups = {}
        for key in sorted(self.builtin):
            parts = key.split('.')
            group = parts[0] if parts else 'other'
            if group not in groups:
                groups[group] = []
            groups[group].append((key, self.ff.get(key)))
        
        for group in sorted(groups.keys()):
            items = groups[group]
            lines.append(f"\n【{group.upper()}】")
            for key, val in items:
                if isinstance(val, bool):
                    val_str = "开" if val else "关"
                elif isinstance(val, (int, float)):
                    val_str = str(val)
                elif isinstance(val, str):
                    val_str = f'"{val}"'
                else:
                    val_str = str(val)
                lines.append(f"  {key}: {val_str}")
        
        lines.append("\n```")
        return "\n".join(lines)
    
    def get(self, key: str) -> str:
        """获取单个配置"""
        if key not in self.builtin:
            return f"❌ 未知配置: {key}\n\n可用命令: `config_manager.py list`"
        
        val = self.ff.get(key)
        
        # 获取描述
        descriptions = {
            'memory.silent_mode': '静默模式（无需确认直接记录）',
            'memory.auto_promote': '自动将重要记忆升级到 L2',
            'memory.auto_cleanup': '自动清理过期记忆',
            'memory.summarize_daily': '每日生成摘要',
            'memory.vector_search': '启用向量搜索',
            'memory.llm_enhance': '使用 LLM 增强记忆',
            'search.cache': '搜索结果缓存',
            'search.fuzzy': '模糊搜索',
            'search.hybrid': '混合搜索（向量+FTS）',
            'search.query_rewrite': '查询重写',
            'push.meow_enabled': '启用 MeoW 推送',
            'push.harmonyos_device': '是否拥有 HarmonyOS 设备',
            'push.dual_channel': '双渠道推送',
            'auto_update.enabled': '启用自动更新',
            'auto_update.auto_install': '自动安装更新（需确认）',
            'ux.silent_mode': '静默模式',
            'ux.detailed_errors': '显示详细错误',
        }
        
        desc = descriptions.get(key, '')
        
        lines = [
            "```",
            f"📌 {key}",
            "=" * 40,
            f"值: {val}",
            f"类型: {type(val).__name__}",
        ]
        if desc:
            lines.append(f"说明: {desc}")
        lines.append("```")
        
        return "\n".join(lines)
    
    def set(self, key: str, value) -> str:
        """设置配置"""
        if key not in self.builtin:
            return f"❌ 未知配置: {key}"
        
        orig_value = value
        # 类型转换
        if value.lower() in ('true', '1', 'on', 'yes', '开', '启用'):
            value = True
        elif value.lower() in ('false', '0', 'off', 'no', '关', '禁用'):
            value = False
        elif '.' in value and value.replace('.', '').isdigit():
            value = float(value) if '.' in value else int(value)
        elif value.isdigit():
            value = int(value)
        
        self.ff.set(key, value)
        return f"✅ 已设置: {key} = {orig_value}\n\n立即生效，无需重启。"
    
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
        if not isinstance(val, bool):
            return f"⚠️ {key} 不是布尔值，无法切换\n当前值: {val}"
        
        new_val = not val
        self.ff.set(key, new_val)
        status = "启用" if new_val else "禁用"
        return f"✅ 已切换: {key} = {status}"
    
    def search(self, keyword: str) -> str:
        """搜索配置"""
        keyword = keyword.lower()
        matches = [(k, self.ff.get(k)) for k in sorted(self.builtin) if keyword in k.lower()]
        
        if not matches:
            return f"❌ 没有找到包含 '{keyword}' 的配置"
        
        lines = [f"🔍 搜索 '{keyword}' 的结果 ({len(matches)}项):", ""]
        for key, val in matches:
            if isinstance(val, bool):
                val_str = "开" if val else "关"
            else:
                val_str = str(val)
            lines.append(f"  {key}: {val_str}")
        
        return "\n".join(lines)
    
    def export(self) -> str:
        """导出配置为 JSON"""
        data = {k: self.ff.get(k) for k in sorted(self.builtin)}
        return "```json\n" + json.dumps(data, indent=2, ensure_ascii=False) + "\n```"
    
    def import_config(self, json_str: str) -> str:
        """导入配置"""
        try:
            data = json.loads(json_str)
            count = 0
            for key, val in data.items():
                if key in self.builtin:
                    self.ff.set(key, val)
                    count += 1
            return f"✅ 成功导入 {count} 个配置项"
        except json.JSONDecodeError as e:
            return f"❌ JSON 解析失败: {e}"
    
    def reset(self) -> str:
        """重置所有配置到默认值"""
        # 获取默认值
        defaults = {
            'memory.silent_mode': False,
            'memory.auto_cleanup': True,
            'memory.auto_promote': True,
            'memory.summarize_daily': True,
            'memory.vector_search': True,
            'memory.llm_enhance': False,
            'search.cache': True,
            'search.fuzzy': True,
            'search.hybrid': True,
            'search.query_rewrite': True,
            'ux.silent_mode': True,
            'ux.detailed_errors': True,
            'ux.show_confidence': False,
        }
        
        count = 0
        for key, val in defaults.items():
            if key in self.builtin:
                self.ff.set(key, val)
                count += 1
        
        return f"✅ 已重置 {count} 个配置项到默认值"
    
    def status_report(self) -> str:
        """状态报告"""
        lines = [
            "```",
            "📈 配置状态报告",
            "=" * 40,
            "",
        ]
        
        # 按功能分类统计
        categories = {
            'Memory（记忆）': ['memory.silent_mode', 'memory.auto_promote', 'memory.auto_cleanup', 'memory.summarize_daily', 
                            'memory.vector_search', 'memory.llm_enhance', 'memory.ima_sync'],
            'Search（搜索）': ['search.cache', 'search.fuzzy', 'search.hybrid', 'search.query_rewrite'],
            'Push（推送）': ['push.meow_enabled', 'push.harmonyos_device', 'push.dual_channel'],
            'Auto Update（自动更新）': ['auto_update.enabled', 'auto_update.auto_install'],
            'UX（体验）': ['ux.silent_mode', 'ux.detailed_errors', 'ux.show_confidence'],
            'Experiment（实验）': ['exp.smart_routing', 'exp.persona_update', 'exp.progressive_enable'],
        }
        
        for cat_name, keys in categories.items():
            enabled = sum(1 for k in keys if k in self.builtin and self.ff.get(k) is True)
            total = sum(1 for k in keys if k in self.builtin)
            pct = int(enabled / total * 100) if total > 0 else 0
            bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
            lines.append(f"{cat_name}")
            lines.append(f"  [{bar}] {enabled}/{total} ({pct}%)")
        
        lines.append("")
        
        # 推送渠道状态
        lines.append("【推送渠道】")
        meow_ok = self.ff.get('push.meow_enabled') and self.ff.get('push.harmonyos_device')
        lines.append(f"  负一屏: ✅ 启用")
        lines.append(f"  MeoW: {'✅ 启用' if meow_ok else '⏸️ 未启用'}")
        
        lines.append("\n```")
        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(ConfigManager().dashboard())
        return
    
    cmd = sys.argv[1].lower()
    manager = ConfigManager()
    
    if cmd == 'list':
        print(manager.list_all())
    
    elif cmd == 'get' and len(sys.argv) >= 3:
        print(manager.get(sys.argv[2]))
    
    elif cmd == 'set' and len(sys.argv) >= 4:
        print(manager.set(sys.argv[2], sys.argv[3]))
    
    elif cmd == 'enable' and len(sys.argv) >= 3:
        print(manager.enable(sys.argv[2]))
    
    elif cmd == 'disable' and len(sys.argv) >= 3:
        print(manager.disable(sys.argv[2]))
    
    elif cmd == 'toggle' and len(sys.argv) >= 3:
        print(manager.toggle(sys.argv[2]))
    
    elif cmd == 'search' and len(sys.argv) >= 3:
        print(manager.search(sys.argv[2]))
    
    elif cmd == 'export':
        print(manager.export())
    
    elif cmd == 'reset':
        print(manager.reset())
    
    elif cmd == 'status':
        print(manager.status_report())
    
    elif cmd == 'doctor':
        print(manager.doctor())
    
    elif cmd == 'setup':
        print(manager.setup())
    
    elif cmd == 'help':
        print("""📋 配置管理器命令:

```bash
# 查看仪表盘（推荐）
python3 scripts/config_manager.py

# 列出所有配置
python3 scripts/config_manager.py list

# 获取单个配置详情
python3 scripts/config_manager.py get memory.auto_promote

# 设置配置
python3 scripts/config_manager.py set ux.silent_mode false
python3 scripts/config_manager.py set search.cache true

# 启用/禁用
python3 scripts/config_manager.py enable memory.auto_promote
python3 scripts/config_manager.py disable memory.auto_promote

# 切换配置（布尔值）
python3 scripts/config_manager.py toggle ux.silent_mode

# 搜索配置
python3 scripts/config_manager.py search memory
python3 scripts/config_manager.py search push

# 导出配置
python3 scripts/config_manager.py export

# 状态报告
python3 scripts/config_manager.py status

# 重置到默认值
python3 scripts/config_manager.py reset
```
""")
    
    else:
        print(f"❌ 未知命令: {cmd}")
        print("使用 `config_manager.py help` 查看帮助")


if __name__ == '__main__':
    main()

    def doctor(self) -> str:
        """系统健康检查"""
        lines = ["```", "🏥 yaoyao-memory 系统诊断", "=" * 40, ""]
        issues = []
        
        # 检查1: 配置文件
        config_file = Path(__file__).parent.parent / "config" / "llm_config.json"
        if config_file.exists():
            try:
                cfg = json.loads(config_file.read_text())
                if cfg.get("embedding", {}).get("api_key"):
                    lines.append("✅ Embedding API Key 已配置")
                else:
                    lines.append("⚠️ Embedding API Key 未配置")
                    issues.append("配置 llm_config.json 中的 embedding.api_key")
            except:
                lines.append("❌ 配置文件格式错误")
                issues.append("修复 llm_config.json")
        else:
            lines.append("⚠️ 配置文件不存在（将使用环境变量或 secrets.env）")
        
        # 检查2: Feature Flags
        ff_count = len(self.builtin)
        lines.append(f"✅ Feature Flags: {ff_count} 项")
        
        # 检查3: 关键开关状态
        key_flags = [
            ("memory.auto_promote", "自动升级"),
            ("memory.auto_cleanup", "自动清理"),
            ("search.cache", "搜索缓存"),
            ("push.meow_enabled", "MeoW推送"),
        ]
        lines.append("")
        lines.append("【关键功能】")
        for flag, desc in key_flags:
            val = self.ff.get(flag)
            status = "✅" if val else "❌"
            lines.append(f"  {status} {desc}: {flag}")
        
        # 检查4: 记忆目录
        mem_dir = Path.home() / ".openclaw" / "workspace" / "memory"
        if mem_dir.exists():
            mem_files = list(mem_dir.glob("*.md"))
            lines.append("")
            lines.append(f"✅ 记忆目录: {len(mem_files)} 个文件")
        else:
            lines.append("")
            lines.append("⚠️ 记忆目录不存在")
            issues.append("运行 init_memory.py 初始化")
        
        # 总结
        lines.append("")
        lines.append("=" * 40)
        if issues:
            lines.append("⚠️ 需要关注:")
            for issue in issues:
                lines.append(f"  - {issue}")
            lines.append("")
            lines.append("💡 使用 config_manager.py setup 获取帮助")
        else:
            lines.append("✅ 系统状态正常")
        
        lines.append("```")
        return "\n".join(lines)
    
    def setup(self) -> str:
        """引导式初始化"""
        lines = [
            "```",
            "🚀 yaoyao-memory 初始化向导",
            "=" * 40,
            "",
            "让我们一步步配置好系统:",
            "",
            "【1/4】Embedding API 配置",
            "",
            "推荐创建配置文件:",
            "~/.openclaw/skills/yaoyao-memory/config/llm_config.json",
            "",
            "内容示例:",
            '{',
            '  "embedding": {',
            '    "api_key": "your-api-key",',
            '    "base_url": "https://ai.gitee.com/v1/embeddings",',
            '    "model": "Qwen3-Embedding-8B",',
            '    "dimensions": 1024',
            '  }',
            '  "llm": {',
            '    "api_key": "your-llm-key",',
            '    "base_url": "..."',
            '  }',
            '}',
            "",
            "---",
            "",
            "【2/4】推荐启用功能:",
            "",
        ]
        
        recommendations = [
            ("memory.auto_promote", True, "自动升级重要记忆"),
            ("memory.auto_cleanup", True, "自动清理过期记忆"),
            ("search.cache", True, "启用搜索缓存"),
        ]
        
        for flag, default, desc in recommendations:
            current = self.ff.get(flag)
            status = "✅" if current else "❌"
            recommended = " [推荐]" if default and not current else ""
            lines.append(f"  {status} {desc}: {flag} (当前: {current}){recommended}")
        
        lines.extend([
            "",
            "---",
            "",
            "【3/4】可选: MeoW 推送配置",
            "",
            "如果你有 HarmonyOS 设备:",
            "1. config_manager.py enable push.harmonyos_device",
            "2. config_manager.py enable push.meow_enabled",
            "3. config_manager.py set push.meow_nickname 你的昵称",
            "",
            "---",
            "",
            "【4/4】初始化记忆文件",
            "",
            "运行以下命令:",
            "python3 scripts/init_memory.py",
            "",
            "---",
            "",
            "✅ 初始化完成后:",
            "python3 scripts/health_check.py  # 检查健康",
            "python3 scripts/config_manager.py doctor  # 再次诊断",
            "",
            "```",
        ])
        


# API 兼容层


# 配置名称和描述映射
CONFIG_META = {
    'memory.auto_promote': ('自动升级', '自动将重要记忆升级到 L2', False),
    'memory.auto_cleanup': ('自动清理', '自动清理过期记忆', False),
    'memory.summarize_daily': ('每日摘要', '每日生成摘要', False),
    'memory.vector_search': ('向量搜索', '启用向量搜索', False),
    'memory.llm_enhance': ('LLM增强', '使用 LLM 增强记忆', False),
    'memory.ima_sync': ('IMA同步', '同步到 IMA 云', False),
    'search.hybrid': ('混合搜索', '混合搜索（向量+FTS）', False),
    'search.query_rewrite': ('查询重写', '查询重写', False),
    'search.fuzzy': ('模糊搜索', '模糊搜索', False),
    'search.cache': ('搜索缓存', '搜索结果缓存', False),
    'shell.enabled': ('Shell启用', '启用 Shell 功能', False),
    'shell.whitelist_only': ('白名单模式', '仅允许白名单命令', False),
    'shell.timeout': ('超时时间', '命令超时时间（秒）', False),
    'feedback.enabled': ('反馈启用', '启用反馈功能', False),
    'feedback.auto_adjust': ('自动调整', '自动调整参数', False),
    'ux.silent_mode': ('静默模式', '静默模式', False),
    'ux.show_confidence': ('显示置信度', '显示置信度', False),
    'ux.detailed_errors': ('详细错误', '显示详细错误', False),
    'exp.smart_routing': ('智能路由', '启用智能路由', False),
    'exp.progressive_enable': ('渐进摘要', '启用渐进式摘要', False),
    'exp.persona_update': ('人格更新', '启用人格更新', False),
    'push.meow_enabled': ('MeoW推送', '启用 MeoW 推送', False),
    'push.harmonyos_device': ('HarmonyOS设备', '是否拥有 HarmonyOS 设备', False),
    'push.dual_channel': ('双渠道推送', '双渠道推送', False),
    'push.meow_nickname': ('MeoW昵称', 'MeoW 推送昵称', True),
    'auto_update.enabled': ('自动更新', '启用自动更新', False),
    'auto_update.check_interval': ('检查间隔', '自动更新检查间隔（秒）', False),
    'auto_update.auto_install': ('自动安装', '自动安装更新', False),
    'ab.test_memory_v2': ('内存V2测试', '内存V2测试', False),
    'ab.test_search_v2': ('搜索V2测试', '搜索V2测试', False),
}

def get_config():
    """获取所有配置（Dashboard 格式）"""
    cm = ConfigManager()
    result = {}
    for key in cm.builtin:
        val = cm.ff.get(key)
        name, desc, secret = CONFIG_META.get(key, (key, '', False))
        result[key] = {
            'name': name,
            'desc': desc,
            'value': val,
            'has_value': val is not None,
            'secret': secret
        }
    return result




# 新的分类结构


# =============================================
# 配置分类 - 功能开关
# =============================================
CATEGORIES = {
    'feature': [
        'memory.auto_promote', 'memory.auto_cleanup', 'memory.summarize_daily',
        'memory.vector_search', 'memory.llm_enhance', 'memory.ima_sync',
        'search.hybrid', 'search.query_rewrite', 'search.fuzzy', 'search.cache',
        'shell.enabled', 'shell.whitelist_only', 'shell.timeout',
        'feedback.enabled', 'feedback.auto_adjust',
        'exp.smart_routing', 'exp.progressive_enable', 'exp.persona_update',
        'push.meow_enabled', 'push.harmonyos_device', 'push.dual_channel',
        'ux.silent_mode', 'ux.show_confidence', 'ux.detailed_errors',
        'ab.test_memory_v2', 'ab.test_search_v2',
    ],
    'system': [
        'auto_update.enabled', 'auto_update.auto_install', 'auto_update.check_interval',
    ],
    'push': [
        'push.meow_enabled', 'push.harmonyos_device', 'push.dual_channel', 'push.meow_nickname',
    ],
}

def get_categories():
    """获取配置分类"""
    cm = ConfigManager()
    result = {}
    for cat, keys in CATEGORIES.items():
        valid_keys = [k for k in keys if k in cm.builtin]
        if valid_keys:
            result[cat] = valid_keys
    # 添加其他未分类的配置
    all_keys = set(cm.builtin)
    categorized = set(k for keys in result.values() for k in keys)
    other = sorted(all_keys - categorized)
    if other:
        result['other'] = other
    return result



# =============================================
# API 配置
# =============================================
LLM_CONFIG_FILE = os.path.expanduser("~/.openclaw/workspace/skills/yaoyao-memory-v2/config/llm_config.json")

def get_llm_config():
    try:
        if os.path.exists(LLM_CONFIG_FILE):
            with open(LLM_CONFIG_FILE) as f:
                return json.load(f)
        return {}
    except:
        return {}

def set_llm_config(key: str, value: str):
    try:
        config = get_llm_config()
        parts = key.split('.')
        if len(parts) == 2:
            section, subkey = parts
            if section not in config:
                config[section] = {}
            config[section][subkey] = value
        with open(LLM_CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except:
        return False

API_CONFIG_META = {
    # LLM / Embedding
    'api.llm_api_key': ('LLM API Key', 'LLM API 密钥（推荐 MiniMax-M2.7）', True),
    'api.embedding_api_key': ('Embedding API Key', 'Embedding API 密钥（Gitee AI）', True),
    # 平台 API
    'api.feishu_app_id': ('飞书 App ID', '飞书应用 ID', False),
    'api.feishu_app_secret': ('飞书 App Secret', '飞书应用密钥', True),
    'api.github_token': ('GitHub Token', 'GitHub 访问令牌', True),
    'api.gateway_token': ('Gateway Token', 'Gateway 访问令牌', True),
    'api.tieba_token': ('贴吧 Token', '百度贴吧访问令牌', True),
    # 推送服务
    'api.today_task_auth': ('Today-Task 密钥', 'today-task 推送密钥', True),
    'api.napcat_token': ('NapCat Token', 'QQ 机器人访问令牌', True),
    # 云服务
    'api.ima_client_id': ('IMA Client ID', 'IMA 笔记服务 ID', False),
    'api.ima_api_key': ('IMA API Key', 'IMA 笔记服务密钥', True),
    'api.clawhub_token': ('ClaWHub Token', 'ClaWHub 访问令牌', True),
    'api.meow_nickname': ('MeoW 昵称', 'MeoW 推送昵称', False),
}

def get_api_categories():
    return {
        'api': list(API_CONFIG_META.keys()),
    }



CAT_NAMES = {
    "feature": "功能开关",
    "api": "API 配置",
    "system": "系统配置",
    "push": "推送配置",
    "other": "其他",
}


# 读取实际 API 配置
def get_api_config():
    """获取 API 配置（读取实际值）"""
    result = {}
    # 从 secrets.env 读取
    secrets_file = os.path.expanduser("~/.openclaw/credentials/secrets.env")
    env_vars = {}
    if os.path.exists(secrets_file):
        with open(secrets_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    env_vars[key.strip()] = val.strip().strip('"')
    
    # 映射到 API 配置
    mapping = {
        'api.llm_api_key': env_vars.get('LLM_API_KEY') or env_vars.get('OPENAI_API_KEY'),
        'api.embedding_api_key': env_vars.get('EMBEDDING_API_KEY') or env_vars.get('GITEE_EMBED_API_KEY'),
        'api.feishu_app_id': env_vars.get('FEISHU_APP_ID'),
        'api.feishu_app_secret': env_vars.get('FEISHU_APP_SECRET'),
        'api.github_token': env_vars.get('GITHUB_TOKEN'),
        'api.gateway_token': env_vars.get('GATEWAY_TOKEN'),
        'api.tieba_token': env_vars.get('TB_TOKEN'),
        'api.today_task_auth': env_vars.get('TODAY_TASK_AUTH_CODE'),
        'api.napcat_token': env_vars.get('NAPCAT_ACCESS_TOKEN'),
        'api.ima_client_id': env_vars.get('IMA_CLIENT_ID'),
        'api.ima_api_key': env_vars.get('IMA_API_KEY'),
        'api.clawhub_token': env_vars.get('CLAWHUB_TOKEN'),
        'api.meow_nickname': env_vars.get('MEOW_NICKNAME'),
    }
    
    for key, (name, desc, secret) in API_CONFIG_META.items():
        value = mapping.get(key)
        has_value = value is not None and value != ''
        result[key] = {
            'name': name,
            'desc': desc,
            'value': value if not secret else ('*' * 8 if has_value else None),
            'has_value': has_value,
            'secret': secret
        }
    return result


# =============================================================================
# 密码管理
# =============================================================================

def get_password_hash(password: str) -> str:
    """简单哈希密码（生产环境应使用 bcrypt）"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()


def has_config_password() -> bool:
    """检查是否设置了密码"""
    password_file = Path.home() / ".openclaw" / "memory-tdai" / ".password"
    return password_file.exists()


def set_config_password(password: str) -> bool:
    """设置密码"""
    if not password or len(password) < 4:
        return False
    password_file = Path.home() / ".openclaw" / "memory-tdai" / ".password"
    password_file.parent.mkdir(parents=True, exist_ok=True)
    password_file.write_text(get_password_hash(password))
    return True


def verify_config_password(password: str) -> bool:
    """验证密码"""
    password_file = Path.home() / ".openclaw" / "memory-tdai" / ".password"
    if not password_file.exists():
        return True  # 未设置密码时默认通过
    stored = password_file.read_text().strip()
    return stored == get_password_hash(password)


def remove_config_password() -> bool:
    """删除密码"""
    password_file = Path.home() / ".openclaw" / "memory-tdai" / ".password"
    if password_file.exists():
        password_file.unlink()
    return True


def reset_password() -> bool:
    """重置密码（删除密码文件）"""
    password_file = Path.home() / ".openclaw" / "memory-tdai" / ".password"
    if password_file.exists():
        password_file.unlink()
    return True
