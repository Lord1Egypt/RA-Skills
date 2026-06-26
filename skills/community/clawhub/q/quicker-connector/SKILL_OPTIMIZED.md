---
name: quicker-connector
description: 与 Quicker 自动化工具集成，读取、搜索和执行 Quicker 动作列表。支持 CSV 和数据库双数据源，智能匹配用户需求并调用本地 QuickerStarter 执行。
author: CodeBuddy (optimized by Advanced Skill Creator)
version: 1.2.0
license: MIT
tags:
  - automation
  - productivity
  - quicker
  - windows
  - workflow
trigger:
  - quickre
  - quick
  - 快键
  - 快速
  - 调用.*动作
  - 执行.*quicker
  - 用.*quicker
  - quicker.*帮我
examples:
  - user: "用quicker截图"
    description: 匹配并执行截图相关动作
  - user: "帮我翻译这段文字"
    description: 智能匹配翻译动作
  - user: "quicker搜索包含'搜索'的动作"
    description: 搜索特定关键词的动作
  - user: "列出所有可用的quicker动作"
    description: 获取完整动作列表和统计

requirements:
  python: ">=3.8"
  system:
    - platform: windows
      reason: "依赖 QuickerStarter.exe，仅 Windows 可用"

settings:
  initialized:
    type: boolean
    description: 是否已完成初始化配置
    default: false
  csv_path:
    type: string
    description: Quicker 动作 CSV 文件路径
    default: ""
  db_path:
    type: string
    description: Quicker 数据库路径
    default: "C:\\Users\\Administrator\\AppData\\Local\\Quicker\\data\\quicker.db"
  starter_path:
    type: string
    description: QuickerStarter.exe 路径
    default: "C:\\Program Files\\Quicker\\QuickerStarter.exe"
  default_source:
    type: string
    description: 默认数据源类型
    default: csv
    options:
      - csv
      - db
  encodings:
    type: array
    description: CSV 编码检测顺序
    default:
      - utf-8-sig
      - utf-8
      - gbk
      - gb2312
      - gb18030
      - latin-1
  auto_select_threshold:
    type: number
    description: 自动选择动作的匹配分数阈值
    default: 0.8
    minimum: 0.5
    maximum: 1.0
    step: 0.05
  max_results:
    type: number
    description: 最大返回结果数量
    default: 10
    minimum: 1
    maximum: 50

system_prompt: |
  你现在是一个 Quicker 自动化专家，具备以下能力：
  - 理解用户的自然语言需求并转化为 Quicker 动作搜索
  - 根据动作名称、描述、类型、分类等多维度智能匹配
  - 精确控制动作执行（同步/异步、参数传递）
  
  重要原则：
  1. 当用户提到"用 quicker 做 X"时，你应理解这是调用 quick 动作完成任务
  2. 优先选择匹配分数 > auto_select_threshold 的动作自动执行
  3. 如果匹配分数低或存在歧义，询问用户确认
  4. 执行前检查 QuickerStarter 是否可用
  5. 向用户清晰说明即将执行的动作及其作用

thinking_model: |
  多阶段认知管线：
  1. 需求解析：提取核心动词和对象（如"截图"、"翻译"）
  2. 上下文识别：是否涉及特定应用（浏览器、Excel、代码编辑器）
  3. 候选筛选：基于类型、面板、关键词三层过滤
  4. 置信度评估：检查最高分是否超过阈值
  5. 决策下达：执行或请求确认

security_notes: |
  - 所有文件操作限制在配置路径和用户数据目录
  - subprocess 调用仅限 QuickerStarter.exe，参数经过验证
  - 无网络访问，不收集用户数据
  - 配置文件仅存储路径，不包含敏感信息
  - CSV/DB 读取使用安全编码检测

---

# Quicker Connector 技能

## 📋 概述

Quicker Connector 是一个专业的 Quicker 集成工具，让你能够通过 AI 助手直接检索、匹配和执行 Quicker 软件中的自动化动作。支持两种数据源模式，智能语义匹配，准确理解用户意图。

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 📊 **双数据源** | 同时支持 CSV 导出文件和 SQLite 数据库 |
| 🔍 **多字段搜索** | 按名称、描述、类型、面板等字段搜索 |
| 🧠 **智能匹配** | 基于关键词提取和语义分析的自动匹配 |
| 🎯 **精确执行** | 支持同步/异步、参数传递、等待结果 |
| 🔧 **编码自适应** | 自动检测 UTF-8/GBK 等多种编码 |
| 📈 **统计信息** | 完整动作分类和面板分布统计 |
| 📤 **JSON 导出** | 一键导出完整动作列表 |

## 🚀 快速开始

### 1️⃣ 首次初始化

运行引导脚本配置 CSV 路径：

```bash
python scripts/init_quicker.py
```

按提示操作：
- 在 Quicker 中导出动作列表（工具 → 导出动作列表(CSV)）
- 将 CSV 文件保存到任意位置
- 输入完整路径完成配置

配置将保存在 `config.json`。

### 2️⃣ 验证安装

```bash
python scripts/test_quicker_connector.py
```

预期看到：
- ✅ 编码检测通过
- ✅ CSV 读取成功，动作数量 > 0
- ✅ 搜索和匹配功能正常
- ✅ QuickerStarter 路径检测

### 3️⃣ 基本使用

```python
from quicker_connector import QuickerConnector

# 创建连接器
connector = QuickerConnector(source="csv")

# 读取所有动作
actions = connector.read_actions()
print(f"共 {len(actions)} 个动作")

# 搜索动作
results = connector.search_actions("截图")
for action in results:
    print(f"- {action.name}")

# 智能匹配
matches = connector.match_actions("帮我翻译这段文字", top_n=3)
for m in matches:
    print(f"{m['action'].name} (分数: {m['score']:.2f})")

# 执行动作
result = connector.execute_action(
    action_id="xxxx",
    wait_for_result=True,
    timeout=10
)
print(f"执行结果: {result.success}, 输出: {result.output}")
```

## 🎯 触发示例

| 用户输入 | 行为 |
|---------|------|
| "用 quicker 截图" | 搜索并推荐截图类动作 |
| "帮我翻译这段文字" | 匹配翻译相关动作 |
| "列出所有 quicker 动作" | 返回完整列表和分类统计 |
| "quicker 执行 ID 为 xxx 的动作" | 直接执行指定动作 |

## 📊 数据结构

### QuickerAction

```python
@dataclass
class QuickerAction:
    id: str                    # 唯一标识
    name: str                  # 动作名称
    description: str           # 描述
    icon: str                  # 图标路径/URL
    action_type: str           # 类型: XAction/SendKeys/RunProgram...
    uri: str                   # 执行 URI (quicker:runaction:xxx)
    panel: str                 # 所属面板/分类
    exe: str                   # 关联程序名
    associated_exe: str        # 关联可执行文件
    position: str              # 在面板中的位置
    size: str                  # 大小
    create_time: str           # 创建时间
    update_time: str           # 更新时间
    source: str                # 来源动作
```

### QuickerActionResult

```python
@dataclass
class QuickerActionResult:
    success: bool              # 是否成功
    output: str                # 标准输出
    error: Optional[str]       # 错误信息
    exit_code: Optional[int]   # 退出码
```

## ⚙️ 配置说明

配置文件 `config.json`（自动生成）：

```json
{
  "csv_path": "/path/to/QuickerActions.csv",
  "initialized": true
}
```

高级设置（通过技能设置界面）：

| 设置项 | 类型 | 默认 | 说明 |
|--------|------|------|------|
| `auto_select_threshold` | float | 0.8 | 自动执行阈值，低于此值会询问用户 |
| `max_results` | int | 10 | 最大返回结果数量 |
| `default_source` | string | "csv" | 数据源类型（csv/db） |

## 🛠️ 高级功能

### 导出 JSON

将完整动作列表导出为 JSON：

```python
connector.export_to_json("actions.json")
```

### 获取统计信息

```python
stats = connector.get_statistics()
print(f"总计: {stats['total']}")
print("类型分布:", stats['by_type'])
print("面板分布:", stats['by_panel'])
```

### 批量执行准备

```python
actions = connector.read_actions()
xaction_only = [a for a in actions if a.action_type == 'XAction']
print(f"可执行 XAction: {len(xaction_only)} 个")
```

## 📝 CSV 格式规范

Quicker 导出的 CSV 文件格式：

```csv
sep=,
Id,名称,说明,图标,类型,Uri,动作页,EXE,关联Exe,位置,大小,创建或安装时间,最后更新,来源动作
123,动作名称,动作说明,图标URL,XAction,quicker:runaction:123,默认页,,,0,0,2024-01-01 10:00:00,2024-01-01 10:00:00,
```

**关键字段**：
- `类型`：`XAction`、`SendKeys`、`RunProgram` 等
- `Uri`：`quicker:runaction:<动作ID>` 格式
- `动作页`：动作所属面板/分类

## ⚠️ 系统要求

- **操作系统**: Windows（Quicker 仅支持 Windows）
- **Quicker 版本**: v2.0+
- **权限**: 需要访问 `QuickerStarter.exe`
- **Python**: 3.8+

## 🔒 安全说明

- 所有文件操作仅访问用户指定的路径
- subprocess 调用严格限制为 QuickerStarter.exe
- 不收集或传输任何用户数据
- 无网络访问权限
- 配置文件中不存储敏感信息

## 🐛 故障排除

| 问题 | 解决方案 |
|------|----------|
| `FileNotFoundError` | 检查 CSV/DB 路径是否正确 |
| 编码错误 | 在设置中调整 `encodings` 顺序 |
| QuickerStarter 未找到 | 手动配置 `starter_path` |
| 动作执行失败 | 检查动作 ID 和权限，确保 Quicker 正在运行 |

## 📚 参考资料

- [Quicker 官网](https://getquicker.net/)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [技能开发指南](https://docs.clawd.bot/tools/skills)

## 📄 许可证

MIT License - 详见 LICENSE 文件（如有）
