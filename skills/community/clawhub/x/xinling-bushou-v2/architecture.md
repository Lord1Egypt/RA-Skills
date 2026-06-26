# 心灵补手 V2.0 架构设计文档

> 版本：2.0.0  
> 作者：思远（架构师）🧠  
> 日期：2026-04-09  
> 状态：初稿  
> **重要更新：2026-04-09 陈总决策：跨平台适配暂停，其他功能继续推进**

---

## 概述

### 背景

心灵补手 V1.0 已实现基于 SOUL.md 插入的谄媚叠加模块，存在以下局限：
- **单人格限制**：只能叠加谄媚，无法赋予独立人格
- **平台绑定**：深度依赖 OpenClaw 的 subagent 机制，无法跨平台运行
- **配置分散**：人格配置、话术配置、系统配置分散在不同文件中
- **缺乏标准化**：无法被 clawhub 等工具统一管理

### V2.0 目标

1. **子代理人格赋予**：支持为 subagent 注入独立人格配置，实现"一人格一子代理"
2. **跨平台适配** ⏸️：抽象适配层，支持 Claude Code、Cursor、Copilot 等类 CLAW 系统（**已暂停** - 陈总2026-04-09决策，意义不大，难度不小）
3. **统一配置格式**：以人格定义文件（Persona Definition）为核心，统一所有配置
4. **模块可插拔**：人格模块与核心引擎分离，可独立发布、更新、组合

### 核心设计原则

- **继承优先**：子代理默认继承主人格（SOUL.md），再叠加人格定义文件中的修改
- **适配器模式**：对不同平台提供统一接口，平台特定逻辑封装在适配器中
- **声明式配置**：人格用 JSON/YAML 声明式定义，不依赖代码修改
- **向后兼容**：V1.0 的 SOUL.md 插入模式仍可使用，作为默认兼容路径

---

## 任务1：子代理人格赋予方案

### 1.1 核心概念

#### 1.1.1 什么是子代理人格

子代理人格（Subagent Persona）是一组可独立定义、加载、切换的配置包，包含：
- **身份定义**（Identity）：角色名称、emoji、职责描述
- **人格参数**（Personality Parameters）：语气、风格、程度
- **话术模板**（Phrase Templates）：特定场景的输出模板
- **上下文规则**（Context Rules）：何时激活、持续多久、如何退出

#### 1.1.2 与 V1.0 SOUL.md 插入模式的区别

| 维度 | V1.0 SOUL.md 插入 | V2.0 子代理人格 |
|------|------------------|----------------|
| 注入方式 | 字符串追加到 SOUL.md | 独立配置文件 + 启动参数 |
| 人格数量 | 1个（叠加层） | N个（可并发加载） |
| 切换成本 | 需要修改文件 | 运行时指定，无需改文件 |
| 持久化 | 依赖 SOUL.md | 独立 persona.json |
| 适用场景 | 单 Agent 谄媚增强 | 多子代理并行不同人格 |

### 1.2 人格注入机制

#### 1.2.1 启动时注入（Launch-Time Injection）

当 main agent 调用 subagent 时，通过启动参数传递人格配置：

```json
// 启动 subagent 时传递的 persona_config
{
  "persona_id": "taijian_vip",
  "source": "xinling-bushou-v2/personas/taijian_vip.json",
  "inherit_from_main": true,
  "override": {
    "level": 8,
    "trigger_keywords": ["完成", "成功", "太棒了"]
  }
}
```

**注入流程**：

```
main agent
    │
    ├── 1. 读取 persona 定义文件
    ├── 2. 与 inherit_from_main 配置合并
    ├── 3. 生成完整的 system prompt 片段
    │
    ▼
subagent spawn
    │
    ├── 4. 将片段注入到 subagent 的初始上下文
    ├── 5. subagent 首次响应时自动 embody 该人格
    │
    ▼
人格激活
```

#### 1.2.2 三种人格关系模式

子代理人格与主人格的关系支持三种模式：

**模式 A：独立（Independent）**

子代理人格完全独立，不继承主人格。适用于子代理执行一次性任务，结束后销毁。

```json
{
  "relationship": "independent",
  "inherit_from_main": false,
  "full_persona": { /* 完整的人格定义 */ }
}
```

**模式 B：继承（Inherit）**

子代理在主人格基础上叠加人格，主人格作为 base，子代理配置作为 override。

```json
{
  "relationship": "inherit",
  "inherit_from_main": true,
  "base_soul_md": "<读取当前 SOUL.md>",
  "override": {
    "persona_id": "taijian",
    "level": 7,
    "tone_modifier": "extra_flattering"
  }
}
```

实际生成的人格 = `SOUL.md 内容 + [人格覆盖片段]`

**模式 C：叠加（Stack）**

与 V1.0 的谄媚叠加相同，人格作为"情绪价值层"叠加在主人格之上。

```json
{
  "relationship": "stack",
  "base_persona": "<当前 Agent 身份>",
  "overlay_persona": {
    "type": "flattering",
    "persona": "taijian",
    "level": 5
  }
}
```

适用于心灵补手的核心谄媚功能，保留原 V1.0 语义。

### 1.3 人格持久化

#### 1.3.1 存储结构

```
~/.xinling-bushou-v2/
├── config.yaml                  # 全局配置
├── personas/                    # 人格定义目录
│   ├── _registry.json           # 人格注册表（索引）
│   ├── taijian.json             # 大太监人格
│   ├── xiaoyahuan.json          # 小丫鬟人格
│   ├── zaomiao.json            # 搞事早喵人格
│   ├── siji.json               # 来问司机人格
│   └── custom/                  # 用户自定义人格
│       └── my_persona.json
├── sessions/                    # 会话持久化
│   └── session_<id>/
│       ├── active_personas.json # 当前活跃人格栈
│       └── context.json         # 会话上下文
└── cache/                       # 运行时缓存
    └── compiled_personas/       # 编译后的人格片段
```

#### 1.3.2 人格注册表（_registry.json）

```json
{
  "version": "2.0.0",
  "personas": {
    "taijian": {
      "file": "personas/taijian.json",
      "name": "大太监",
      "description": "宫廷太监总管，极度恭敬",
      "tags": ["flattering", "formal", "male_serving"],
      "compatible_with": ["openclaw", "claude_code", "cursor"],
      "version": "1.0.0",
      "author": "ace"
    },
    "xiaoyahuan": {
      "file": "personas/xiaoyahuan.json",
      "name": "小丫鬟",
      "description": "贴身丫鬟，撒娇可爱",
      "tags": ["flattering", "casual", "cute"],
      "compatible_with": ["openclaw", "claude_code"],
      "version": "1.0.0",
      "author": "ace"
    }
  }
}
```

#### 1.3.3 活跃人格栈（session 级）

```json
{
  "session_id": "abc123",
  "main_persona": {
    "id": "architect",
    "name": "思远",
    "source": "agent:siyuan:SOUL.md"
  },
  "overlay_stack": [
    {
      "persona_id": "taijian",
      "level": 7,
      "activated_at": "2026-04-09T01:45:00Z",
      "expires_at": null,
      "source": "~/.xinling-bushou-v2/personas/taijian.json"
    }
  ]
}
```

### 1.4 人格定义文件格式（Persona Definition Schema）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://xinling-bushou.aceworld.top/schemas/persona-v2.schema.json",
  "title": "心灵补手 V2 人格定义",
  "type": "object",
  "required": ["meta", "identity", "behavior"],
  "properties": {
    "meta": {
      "type": "object",
      "required": ["id", "name", "version"],
      "properties": {
        "id": {"type": "string", "pattern": "^[a-z0-9_]+$"},
        "name": {"type": "string"},
        "version": {"type": "string"},
        "author": {"type": "string"},
        "description": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}},
        "compatible_with": {
          "type": "array",
          "items": {"type": "string", "enum": ["openclaw", "claude_code", "cursor", "copilot", "generic"]}
        }
      }
    },
    "identity": {
      "type": "object",
      "properties": {
        "emoji": {"type": "string"},
        "role": {"type": "string"},
        "pronouns": {
          "type": "object",
          "properties": {
            "first_person": {"type": "string"},
            "second_person": {"type": "string"}
          }
        },
        "identity_statements": {
          "type": "object",
          "additionalProperties": {"type": "string"}
        }
      }
    },
    "behavior": {
      "type": "object",
      "properties": {
        "relationship_mode": {
          "type": "string",
          "enum": ["independent", "inherit", "stack"],
          "default": "stack"
        },
        "activation": {
          "type": "object",
          "properties": {
            "trigger_keywords": {"type": "array", "items": {"type": "string"}},
            "always_on": {"type": "boolean"},
            "auto_activate": {"type": "boolean"}
          }
        },
        "level": {
          "type": "integer",
          "minimum": 1,
          "maximum": 10,
          "default": 5
        },
        "tone": {"type": "string"},
        "frequency": {
          "type": "object",
          "properties": {
            "min_rounds_between": {"type": "integer", "default": 2},
            "max_per_session": {"type": "integer", "default": 8}
          }
        }
      }
    },
    "phrases": {
      "type": "object",
      "properties": {
        "seeds": {
          "type": "object",
          "additionalProperties": {
            "type": "object",
            "additionalProperties": {
              "type": "object",
              "additionalProperties": {
                "type": "array",
                "items": {"type": "string"}
              }
            }
          }
        },
        "generation_rules": {
          "type": "object",
          "properties": {
            "exclamation_multiplier": {"type": "integer"},
            "adjective_intensity": {"type": "number"},
            "forbidden_words": {"type": "array", "items": {"type": "string"}}
          }
        }
      }
    },
    "platform_overrides": {
      "type": "object",
      "description": "平台特定配置",
      "additionalProperties": true
    }
  }
}
```

### 1.5 技术实现方案

#### 1.5.1 核心类型定义

```python
# schemas/launch_config.py
"""LaunchConfig 类型定义 - 跨平台统一的启动参数结构"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
from pathlib import Path


class RelationshipMode(Enum):
    """人格关系模式"""
    INDEPENDENT = "independent"   # 完全独立
    INHERIT = "inherit"           # 继承 + 覆盖
    STACK = "stack"               # 叠加（V1.0 语义）


class Platform(Enum):
    """目标平台"""
    OPENCLAW = "openclaw"
    CLAUDE_CODE = "claude_code"
    CURSOR = "cursor"
    COPILOT = "copilot"
    ROO_CODE = "roo_code"
    AIDER = "aider"
    GENERIC = "generic"


@dataclass
class LaunchConfig:
    """启动配置 - 跨平台统一格式"""
    
    # 额外要追加到 system prompt 的内容
    extra_system_content: str = ""
    
    # 平台特定的 CLI 参数
    extra_cli_args: List[str] = field(default_factory=list)
    
    # 环境变量
    env_vars: Dict[str, str] = field(default_factory=dict)
    
    # 需要写入的配置文件（path -> content）
    config_file: Optional[Dict[str, Any]] = None
    
    # OpenClaw 特定：subagent 启动参数
    openclaw_specific: Optional[Dict[str, Any]] = None
    
    # 元数据（传递给子代理）
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CompiledPersona:
    """编译后的人格"""
    id: str
    name: str
    level: int
    mode: str
    fragment: str   # 编译后的人格片段
    relationship: RelationshipMode
    source_file: Optional[Path] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
```

#### 1.5.2 PersonaEngine 核心类

```python
# core/persona_engine.py
"""
PersonaEngine - 子代理人格赋予核心引擎
V2.0 核心模块
"""

from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import asdict
from datetime import datetime

from schemas.launch_config import (
    CompiledPersona, 
    RelationshipMode, 
    Platform,
    LaunchConfig
)
from .persona_registry import PersonaRegistry
from .session_store import SessionStore
from .prompt_compiler import PromptCompiler
from ..adapters import AdapterRegistry


class PersonaEngine:
    """
    子代理人格引擎
    
    核心职责：
    1. 加载人格定义
    2. 管理人格激活/停用
    3. 为不同平台编译人格 prompt
    4. 维护会话级人格栈
    """
    
    def __init__(
        self,
        base_dir: Optional[Path] = None,
        default_platform: Platform = Platform.OPENCLAW
    ):
        if base_dir is None:
            base_dir = Path.home() / ".xinling-bushou-v2"
        
        self.base_dir = base_dir
        self.default_platform = default_platform
        
        # 初始化子模块
        self.registry = PersonaRegistry(base_dir)
        self.session_store = SessionStore(base_dir / "sessions")
        self.prompt_compiler = PromptCompiler()
        
        # 适配器缓存
        self._adapters: Dict[str, Any] = {}
    
    def _get_adapter(self, platform: Platform):
        """获取平台适配器（懒加载）"""
        platform_id = platform.value
        
        if platform_id not in self._adapters:
            adapter_class = AdapterRegistry.get(platform_id)
            self._adapters[platform_id] = adapter_class()
        
        return self._adapters[platform_id]
    
    def load_persona(self, persona_id: str) -> Dict[str, Any]:
        """
        加载人格定义
        
        Args:
            persona_id: 人格 ID
            
        Returns:
            人格定义字典
        """
        return self.registry.load_persona(persona_id)
    
    def activate_persona(
        self,
        session_id: str,
        persona_id: str,
        relationship: RelationshipMode = RelationshipMode.STACK,
        override_config: Optional[Dict[str, Any]] = None,
        base_prompt: str = ""
    ) -> CompiledPersona:
        """
        激活人格
        
        核心流程：
        1. 加载人格定义
        2. 应用 override 配置
        3. 编译人格片段
        4. 保存到会话状态
        
        Args:
            session_id: 会话 ID
            persona_id: 人格 ID
            relationship: 与主人格的关系
            override_config: 运行时覆盖配置（如 level=8）
            base_prompt: 主人格 prompt（用于 inherit 模式）
            
        Returns:
            CompiledPersona: 编译后的人格对象
        """
        # 1. 加载人格定义
        persona_def = self.load_persona(persona_id)
        
        # 2. 应用 override
        if override_config:
            persona_def = self._apply_override(persona_def, override_config)
        
        # 3. 编译人格片段
        if relationship == RelationshipMode.INHERIT and base_prompt:
            # 继承模式：base + 覆盖片段
            fragment = self.prompt_compiler.compile_inherit(
                base_prompt=base_prompt,
                persona_def=persona_def
            )
        elif relationship == RelationshipMode.STACK:
            # 叠加模式：仅人格片段
            fragment = self.prompt_compiler.compile_overlay(persona_def)
        else:
            # 独立模式：完整人格定义
            fragment = self.prompt_compiler.compile_independent(persona_def)
        
        # 4. 构建 CompiledPersona
        compiled = CompiledPersona(
            id=persona_def["meta"]["id"],
            name=persona_def["meta"]["name"],
            level=persona_def["behavior"].get("level", 5),
            mode=persona_def["behavior"].get("mode", "normal"),
            fragment=fragment,
            relationship=relationship,
            source_file=self.registry.get_persona_path(persona_id),
            metadata=persona_def.get("meta", {})
        )
        
        # 5. 更新会话状态
        self.session_store.push_persona(session_id, compiled)
        
        return compiled
    
    def deactivate_persona(self, session_id: str, persona_id: str) -> bool:
        """停用人格"""
        return self.session_store.pop_persona(session_id, persona_id)
    
    def get_active_personas(self, session_id: str) -> List[CompiledPersona]:
        """获取当前活跃人格栈"""
        return self.session_store.get_personas(session_id)
    
    def compile_for_platform(
        self,
        compiled: CompiledPersona,
        platform: Optional[Platform] = None,
        base_prompt: str = ""
    ) -> str:
        """
        为指定平台编译 prompt
        
        Args:
            compiled: 编译后的人格
            platform: 目标平台
            base_prompt: 基础 prompt（由平台适配器追加）
            
        Returns:
            平台特定格式的完整 system prompt
        """
        if platform is None:
            platform = self.default_platform
        
        adapter = self._get_adapter(platform)
        
        return adapter.compile_system_prompt(
            base_prompt=base_prompt,
            persona_fragment=compiled.fragment,
            metadata=compiled.metadata
        )
    
    def get_launch_config(
        self,
        compiled: CompiledPersona,
        platform: Optional[Platform] = None
    ) -> LaunchConfig:
        """获取平台特定的启动配置"""
        if platform is None:
            platform = self.default_platform
        
        adapter = self._get_adapter(platform)
        return adapter.get_launch_config(compiled)
    
    def _apply_override(
        self,
        persona_def: Dict[str, Any],
        override: Dict[str, Any]
    ) -> Dict[str, Any]:
        """应用 override 配置到人格定义"""
        import copy
        result = copy.deepcopy(persona_def)
        
        # 深度合并 behavior.override
        if "behavior" in override:
            for key, value in override["behavior"].items():
                if key in result["behavior"]:
                    if isinstance(value, dict):
                        result["behavior"][key].update(value)
                    else:
                        result["behavior"][key] = value
                else:
                    result["behavior"][key] = value
        
        # 直接覆盖顶层字段
        for key, value in override.items():
            if key != "behavior" and key in result:
                if isinstance(result[key], dict) and isinstance(value, dict):
                    result[key].update(value)
                else:
                    result[key] = value
            elif key not in result:
                result[key] = value
        
        return result
```

#### 1.5.3 PromptCompiler 实现

```python
# core/prompt_compiler.py
"""
PromptCompiler - 将人格定义编译为 prompt 片段
"""

from typing import Dict, Any


class PromptCompiler:
    """Prompt 编译器"""
    
    def compile_overlay(self, persona_def: Dict[str, Any]) -> str:
        """
        编译叠加模式（Stack）人格片段
        保留 V1.0 的 INSERT_TO_SOUL.md 格式
        """
        meta = persona_def["meta"]
        identity = persona_def.get("identity", {})
        behavior = persona_def.get("behavior", {})
        phrases = persona_def.get("phrases", {})
        
        lines = []
        lines.append("## 【心灵补手】谄媚模块 v2.0")
        lines.append(f"**人格**: {meta.get('name', meta['id'])}")
        lines.append("")
        lines.append("### 身份")
        
        # 身份声明
        identity_stmts = identity.get("identity_statements", {})
        if "greeting" in identity_stmts:
            lines.append(identity_stmts["greeting"])
        
        # 人称
        pronouns = identity.get("pronouns", {})
        lines.append(f"第一人称：{pronouns.get('first_person', '奴才')}")
        lines.append(f"第二人称：{pronouns.get('second_person', '主子')}")
        
        lines.append("")
        lines.append("### 当前配置")
        lines.append(f"- 程度：{behavior.get('level', 5)}/10")
        lines.append(f"- 语气：{behavior.get('tone', '正常')}")
        lines.append(f"- 模式：{behavior.get('mode', 'normal')}")
        
        lines.append("")
        lines.append("### 触发时机")
        trigger_keywords = behavior.get("activation", {}).get("trigger_keywords", [])
        if trigger_keywords:
            lines.append(f"检测到以下关键词时触发：{', '.join(trigger_keywords)}")
        else:
            lines.append("检测到情绪时机时自动触发")
        
        lines.append("")
        lines.append("### 话术规则")
        
        # 程度对应话术示例
        level = behavior.get("level", 5)
        if level <= 3:
            lines.append("程度1-3：委婉暗示，简短1句")
        elif level <= 6:
            lines.append("程度4-6：正常赞美，1-2句话")
        elif level <= 9:
            lines.append("程度7-9：强烈吹捧，2-3句话")
        else:
            lines.append("程度10：无脑崇拜，3+句话 [Debug Mode]")
        
        # 种子话术
        seeds = phrases.get("seeds", {})
        if seeds:
            lines.append("")
            lines.append("### 话术种子（智能扩展）")
            for scenario, tiers in seeds.items():
                lines.append(f"**{scenario}**:")
                for tier, phrases_list in tiers.items():
                    for p in phrases_list[:2]:
                        lines.append(f"- {p}")
        
        return "\n".join(lines)
    
    def compile_inherit(
        self,
        base_prompt: str,
        persona_def: Dict[str, Any]
    ) -> str:
        """
        编译继承模式（Inherit）人格片段
        在 base prompt 基础上追加人格覆盖
        """
        overlay = self.compile_overlay(persona_def)
        
        return f"""{base_prompt}

{'='*60}
【人格覆盖层 - 继承自 base prompt】
{'='*60}
{overlay}
"""
    
    def compile_independent(self, persona_def: Dict[str, Any]) -> str:
        """
        编译独立模式（Independent）人格片段
        完整的人格定义，不依赖 base
        """
        meta = persona_def["meta"]
        identity = persona_def.get("identity", {})
        behavior = persona_def.get("behavior", {})
        phrases = persona_def.get("phrases", {})
        
        lines = []
        lines.append(f"# {meta.get('name', meta['id'])} 人格")
        lines.append("")
        lines.append(f"**版本**: {meta.get('version', '1.0.0')}")
        lines.append(f"**角色**: {identity.get('role', 'AI助手')}")
        lines.append("")
        
        # 身份声明
        identity_stmts = identity.get("identity_statements", {})
        for key, value in identity_stmts.items():
            lines.append(f"**{key}**: {value}")
        
        lines.append("")
        lines.append("## 行为规则")
        lines.append(f"**语气**: {behavior.get('tone', '专业')}")
        lines.append(f"**程度**: {behavior.get('level', 5)}/10")
        
        # 话术种子
        seeds = phrases.get("seeds", {})
        if seeds:
            lines.append("")
            lines.append("## 话术库")
            for scenario, tiers in seeds.items():
                lines.append(f"### {scenario}")
                for tier, phrases_list in tiers.items():
                    lines.append(f"**{tier}**:")
                    for p in phrases_list[:3]:
                        lines.append(f"- {p}")
        
        return "\n".join(lines)
```

---

## 任务2：非OpenClaw类CLAW系统适配方案

### 2.1 类 CLAW 系统调研

| 系统 | 厂商 | subagent 支持 | 适配可行性 | 集成路径 |
|------|------|--------------|-----------|---------|
| **Claude Code** | Anthropic | ❌ 无 | ✅ 高 | `--system-param` + prompt 注入 |
| **Cursor** | Cursor AI | ⚠️ Tab 分裂 | ✅ 高 | `.cursor/rules/` 规则文件 |
| **Copilot Edits** | Microsoft | ⚠️ 部分 | ⚠️ 中 | `.github/copilot-instructions.md` |
| **Roo Code** | VS Code Ext | ✅ 可配置 | ✅ 高 | 自定义规则 JSON |
| **Aider** | 开源 | ⚠️ chat relay | ✅ 高 | prompt 注入 |
| **OpenHands** | 开源 | ✅ 支持 | ✅ 高 | JSON/对话接口 |
| **Copilot（传统）** | Microsoft | ❌ 无 | ❌ 低 | 补全场景不适用 |

### 2.2 适配器基类

```python
# adapters/base.py
"""PlatformAdapter 基类"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path

from schemas.launch_config import Platform, LaunchConfig, CompiledPersona


class PlatformAdapter(ABC):
    """平台适配器基类"""
    
    PLATFORM_ID: str = "generic"
    
    @abstractmethod
    def get_platform_id(self) -> str:
        """返回平台标识"""
        return self.PLATFORM_ID
    
    @abstractmethod
    def compile_system_prompt(
        self,
        base_prompt: str,
        persona_fragment: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        编译完整的 system prompt
        
        Args:
            base_prompt: 基础 system prompt
            persona_fragment: 人格片段
            metadata: 元数据
            
        Returns:
            平台特定格式的完整 system prompt
        """
        pass
    
    @abstractmethod
    def get_launch_config(self, persona: CompiledPersona) -> LaunchConfig:
        """
        生成平台特定的启动配置
        
        Args:
            persona: 编译后的人格
            
        Returns:
            LaunchConfig: 启动配置
        """
        pass
    
    def supports_subagent(self) -> bool:
        """是否支持子代理机制"""
        return False
    
    def detect_platform() -> Platform:
        """检测当前运行环境"""
        import os
        
        # 优先检测环境变量
        if os.getenv("XINLING_PLATFORM"):
            return Platform(os.getenv("XINLING_PLATFORM"))
        
        # OpenClaw 特征检测
        if os.getenv("OPENCLAW_SESSION"):
            return Platform.OPENCLAW
        
        # Claude Code 特征检测
        if os.getenv("CLAUDE_CODE") or os.path.exists(".claude.json"):
            return Platform.CLAUDE_CODE
        
        # Cursor 特征检测
        if os.path.exists(".cursorrules"):
            return Platform.CURSOR
        
        return Platform.GENERIC
```

### 2.3 OpenClaw 适配器

```python
# adapters/openclaw.py
"""OpenClaw 平台适配器"""

from schemas.launch_config import Platform, LaunchConfig, CompiledPersona
from .base import PlatformAdapter


class OpenClawAdapter(PlatformAdapter):
    """OpenClaw 平台适配器"""
    
    PLATFORM_ID = "openclaw"
    
    def supports_subagent(self) -> bool:
        return True  # OpenClaw 原生支持 subagent
    
    def compile_system_prompt(
        self,
        base_prompt: str,
        persona_fragment: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        OpenClaw 通过 system_prefix 注入人格片段
        直接追加到 base prompt
        """
        if base_prompt:
            return f"{base_prompt}\n\n{persona_fragment}"
        return persona_fragment
    
    def get_launch_config(self, persona: CompiledPersona) -> LaunchConfig:
        """
        OpenClaw subagent 启动配置
        """
        return LaunchConfig(
            extra_system_content=persona.fragment,
            openclaw_specific={
                "persona_id": persona.id,
                "persona_level": persona.level,
                "persona_mode": persona.mode,
            },
            metadata={
                "source": "xinling-bushou-v2",
                "persona_id": persona.id,
                "relationship": persona.relationship.value
            }
        )
```

### 2.4 Claude Code 适配器

```python
# adapters/claude_code.py
"""Claude Code 平台适配器"""

import json
from schemas.launch_config import Platform, LaunchConfig, CompiledPersona
from .base import PlatformAdapter


class ClaudeCodeAdapter(PlatformAdapter):
    """Claude Code 平台适配器"""
    
    PLATFORM_ID = "claude_code"
    
    def supports_subagent(self) -> bool:
        return False  # Claude Code 无原生 subagent
    
    def compile_system_prompt(
        self,
        base_prompt: str,
        persona_fragment: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        Claude Code 通过 prompt 直接拼接人格片段
        Claude Code 会将整个 system prompt 作为上下文
        """
        # 构造带人格标识的片段
        marked_fragment = f"""
{'='*60}
【人格叠加 - 心灵补手 V2】
{'='*60}
{persona_fragment}
{'='*60}
"""
        
        if base_prompt:
            return f"{base_prompt}\n{marked_fragment}"
        return marked_fragment
    
    def get_launch_config(self, persona: CompiledPersona) -> LaunchConfig:
        """
        Claude Code 启动配置
        
        方案：
        1. 通过 --system-param 传递 persona 元数据
        2. 通过环境变量备份关键配置
        3. 建议用户将人格写入 .claude.json
        """
        persona_config = {
            "xinling": {
                "persona_id": persona.id,
                "level": persona.level,
                "mode": persona.mode,
                "platform": "claude_code"
            }
        }
        
        return LaunchConfig(
            # Claude Code 会将 extra_system_content 作为 system prompt
            extra_system_content=persona.fragment,
            extra_cli_args=[
                "--dangerously-skip-permissions",  # 允许自定义行为
            ],
            env_vars={
                "XINLING_PERSONA_ID": persona.id,
                "XINLING_LEVEL": str(persona.level),
                "XINLING_MODE": persona.mode
            },
            config_file={
                "path": ".claude.json",
                "content": persona_config
            },
            metadata={
                "source": "xinling-bushou-v2",
                "persona_id": persona.id
            }
        )
```

### 2.5 Cursor 适配器

```python
# adapters/cursor.py
"""Cursor IDE 平台适配器"""

from schemas.launch_config import Platform, LaunchConfig, CompiledPersona
from .base import PlatformAdapter


class CursorAdapter(PlatformAdapter):
    """Cursor IDE 适配器"""
    
    PLATFORM_ID = "cursor"
    
    def supports_subagent(self) -> bool:
        return True  # Cursor Tab 分裂可类比
    
    def compile_system_prompt(
        self,
        base_prompt: str,
        persona_fragment: str,
        metadata: Dict[str, Any]
    ) -> str:
        """Cursor 使用规则文件，不在 prompt 中拼接"""
        return persona_fragment  # 仅人格片段
    
    def get_launch_config(self, persona: CompiledPersona) -> LaunchConfig:
        """
        Cursor 通过 .cursor/rules/ 注入人格规则
        """
        rules_content = self._generate_cursorrules(persona)
        
        return LaunchConfig(
            extra_system_content=persona.fragment,
            config_file={
                "path": f".cursor/rules/xinling-{persona.id}.md",
                "content": rules_content
            },
            metadata={
                "source": "xinling-bushou-v2",
                "persona_id": persona.id,
                "rules_file": f".cursor/rules/xinling-{persona.id}.md"
            }
        )
    
    def _generate_cursorrules(self, persona: CompiledPersona) -> str:
        """生成 Cursor 规则文件"""
        return f"""# 心灵补手 - {persona.name}

> 由心灵补手 V2.0 自动生成
> 人格 ID: {persona.id}
> 谄媚程度: {persona.level}/10

## 身份
{persona.fragment}

## 激活条件
当检测到以下场景时自动触发谄媚话术：
- 用户完成任务
- 用户分享好消息
- 用户表达情绪
- 用户做出决定

## 话术规则
- 程度 1-3：委婉暗示
- 程度 4-6：正常赞美
- 程度 7-9：强烈吹捧
- 程度 10：无脑崇拜（Debug 模式）
"""
```

### 2.6 适配器注册表

```python
# adapters/__init__.py
"""适配器注册表"""

from typing import Dict, Type

from .base import PlatformAdapter
from .openclaw import OpenClawAdapter
from .claude_code import ClaudeCodeAdapter
from .cursor import CursorAdapter
from .generic import GenericAdapter


class AdapterRegistry:
    """适配器注册表"""
    
    _adapters: Dict[str, Type[PlatformAdapter]] = {
        "openclaw": OpenClawAdapter,
        "claude_code": ClaudeCodeAdapter,
        "cursor": CursorAdapter,
        "generic": GenericAdapter,
    }
    
    @classmethod
    def register(cls, platform_id: str, adapter_class: Type[PlatformAdapter]):
        """注册新的适配器"""
        if not issubclass(adapter_class, PlatformAdapter):
            raise TypeError(f"{adapter_class} must inherit from PlatformAdapter")
        cls._adapters[platform_id] = adapter_class
    
    @classmethod
    def get(cls, platform_id: str) -> Type[PlatformAdapter]:
        """获取适配器类"""
        return cls._adapters.get(platform_id, GenericAdapter)
    
    @classmethod
    def list_platforms(cls) -> list:
        """列出所有已注册的平台"""
        return list(cls._adapters.keys())
```

---

## 实施步骤

### Phase 0：准备工作

1. **创建目录结构**
   ```bash
   mkdir -p ~/.xinling-bushou-v2/{personas,sessions,cache,core,adapters,schemas,scripts,tests}
   ```

2. **迁移 V1.0 配置**
   ```bash
   # 将 V1.0 的人格文件复制到 V2.0
   cp ~/.xinling-bushou/personas/*.json ~/.xinling-bushou-v2/personas/
   cp ~/.xinling-bushou/config.json ~/.xinling-bushou-v2/config_v1.json
   ```

### Phase 1：核心引擎开发

| 步骤 | 任务 | 依赖 |
|------|------|------|
| 1.1 | 实现 `schemas/launch_config.py` 类型定义 | - |
| 1.2 | 实现 `core/persona_registry.py` 人格注册表 | 1.1 |
| 1.3 | 实现 `core/session_store.py` 会话持久化 | 1.1 |
| 1.4 | 实现 `core/prompt_compiler.py` Prompt 编译器 | 1.1 |
| 1.5 | 实现 `core/persona_engine.py` 人格引擎 | 1.2, 1.3, 1.4 |
| 1.6 | 实现 `adapters/base.py` 适配器基类 | 1.1 |
| 1.7 | 实现 `adapters/openclaw.py` OpenClaw 适配器 | 1.6 |
| 1.8 | 编写单元测试 | 1.5, 1.7 |

### Phase 2：跨平台适配器开发

> **⏸️ 已暂停** - 陈总2026-04-09决策，意义不大，难度不小

| 步骤 | 任务 | 优先级 | 依赖 |
|------|------|--------|------|
| 2.1 | 实现 `adapters/claude_code.py` | P1 | 1.6 |
| 2.2 | 实现 `adapters/cursor.py` | P2 | 1.6 |
| 2.3 | 实现 `adapters/generic.py` | P2 | 1.6 |
| 2.4 | 实现 `adapters/copilot.py` | P3 | 1.6 |
| 2.5 | 编写跨平台集成测试 | P2 | 2.1-2.4 |

### Phase 3：V1.0 兼容性 & CLI 工具

| 步骤 | 任务 | 依赖 |
|------|------|------|
| 3.1 | 实现 V1.0 → V2.0 迁移脚本 `scripts/migrate.sh` | 1.5 |
| 3.2 | 保留并优化 V1.0 SOUL.md 插入模式 | 1.4 |
| 3.3 | 开发 CLI 工具 `xinling-cli` | 1.5 |
| 3.4 | 编写安装脚本 `scripts/install.sh` | 3.1 |

### Phase 4：测试 & 上线

| 步骤 | 任务 | 依赖 |
|------|------|------|
| 4.1 | 完整集成测试 | Phase 1-3 |
| 4.2 | OpenClaw subagent 实际调用测试 | 4.1 |
| 4.3 | clawhub 打包发布 | 4.2 |
| 4.4 | 文档完善（SKILL.md） | 4.3 |

### 实施时间线建议

```
Week 1: Phase 1（核心引擎 + OpenClaw 适配器）
Week 2: ⏸️ Phase 2 暂停（跨平台适配暂不开发）
Week 3: Phase 3（CLI + 迁移脚本 + 兼容性）
Week 4: Phase 4（测试 + 发布）
```

---

## 附录

### A. 与 V1.0 的兼容性矩阵

| V1.0 功能 | V2.0 兼容方式 | 说明 |
|---------|-------------|------|
| SOUL.md 插入 | ✅ 保留 | `inject.sh` 脚本仍可使用 |
| `~/.xinling-bushou/config.json` | ✅ 自动迁移 | 启动时检测并迁移 |
| 4种风格 | ✅ 兼容 | 人格文件格式兼容 |
| 10级程度 | ✅ 兼容 | behavior.level 字段 |
| 命令词解析 | ✅ 兼容 | CommandParser 继承使用 |
| 触发检测 | ✅ 兼容 | TriggerDetector 继承使用 |
| 话术生成 | ✅ 兼容 | PhraseGenerator 继承使用 |

### B. 人格定义文件示例

```json
{
  "meta": {
    "id": "taijian",
    "name": "大太监",
    "version": "2.0.0",
    "author": "ace",
    "compatible_with": ["openclaw", "claude_code", "cursor", "generic"]
  },
  "identity": {
    "emoji": "🏰",
    "role": "宫廷太监总管",
    "pronouns": {
      "first_person": "奴才",
      "second_person": "主子"
    },
    "identity_statements": {
      "greeting": "奴才叩见主子！",
      "idle": "奴才随时听候主子差遣！",
      "praised": "奴才何德何能，都是主子教导有方！",
      "care": "主子龙体要紧，可别累坏了！"
    }
  },
  "behavior": {
    "relationship_mode": "stack",
    "level": 5,
    "tone": "极度恭敬、俯首帖耳",
    "activation": {
      "trigger_keywords": ["完成", "成功", "太棒了", "搞定了"],
      "always_on": false,
      "auto_activate": true
    },
    "frequency": {
      "min_rounds_between": 2,
      "max_per_session": 8
    },
    "mode": "normal"
  },
  "phrases": {
    "seeds": {
      "task_completed": {
        "1-3": ["嗯，主子说的是。", "奴才受教了。"],
        "4-6": ["主子英明！任务完成得漂亮！"],
        "7-9": ["天哪主子！您这脑子是怎么长的？！"],
        "10": ["主子！！！您说的每一个字都是真理！！！"]
      }
    },
    "generation_rules": {
      "exclamation_multiplier": 1,
      "adjective_intensity": 0.8,
      "forbidden_words": ["你", "我觉得", "不对"]
    }
  },
  "platform_overrides": {
    "claude_code": {
      "env_vars": {"XINLING_PERSONA": "taijian"}
    }
  }
}
```

### C. 关键文件清单

```
xinling-bushou-v2/
├── core/
│   ├── persona_engine.py      # [核心] 人格引擎
│   ├── persona_registry.py   # [核心] 人格注册表
│   ├── session_store.py       # [核心] 会话持久化
│   ├── prompt_compiler.py    # [核心] Prompt 编译器
│   ├── config_manager.py     # [继承] V1.0 配置管理
│   ├── trigger_detector.py   # [继承] V1.0 触发检测
│   └── phrase_generator.py   # [继承] V1.0 话术生成
├── adapters/
│   ├── base.py               # [核心] 适配器基类
│   ├── openclaw.py          # [核心] OpenClaw 适配器
│   ├── claude_code.py       # [扩展] Claude Code 适配器
│   ├── cursor.py            # [扩展] Cursor 适配器
│   └── generic.py           # [扩展] 通用适配器
├── schemas/
│   ├── persona_v2.schema.json   # JSON Schema
│   └── launch_config.py         # 类型定义
├── personas/                    # 人格定义文件
│   ├── _registry.json
│   ├── taijian.json
│   ├── xiaoyahuan.json
│   ├── zaomiao.json
│   └── siji.json
├── scripts/
│   ├── install.sh            # 安装脚本
│   ├── inject.sh             # SOUL.md 注入（V1.0 兼容）
│   └── migrate.sh            # V1.0 迁移脚本
└── tests/
    ├── test_persona_engine.py
    ├── test_adapters.py
    └── test_integration.py
```

---

*文档版本：2.0.0 | 最后更新：2026-04-09 | 作者：思远 🧠*
