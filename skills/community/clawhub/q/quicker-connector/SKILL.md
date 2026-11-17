---
name: quicker-connector
description: 与 Quicker 自动化工具集成，读取、搜索和执行 Quicker 动作列表。支持 CSV 和数据库双数据源，智能匹配用户需求并调用本地 QuickerStarter 执行。同时提供数据维护能力：解析维护工具全量备份（export 目录）、按配置映射定位/读取/修改快捷键、轮盘、手势、组合键等所有配置。并可将「程序/脚本/命令」一键生成 Quicker「运行程序或打开文件」(ActionType 11) 的可导入动作 JSON（智能起名、自动探测解释器、日志重定向）。
author: CodeBuddy (optimized by Advanced Skill Creator)
version: 1.6.0
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
  - user: "quicker的扩展热键配置在哪里"
    description: 用配置映射定位快捷键配置
  - user: "把左键+C改成复制"
    description: 读取并修改左键增强配置
  - user: "怎么全量导出quicker配置"
    description: 指导维护工具备份并生成映射
  - user: "帮我把 potplayer_clip.py 做成 quicker 启动动作"
    description: 生成可导入的『运行程序或打开文件』动作 JSON

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
| 🚀 **生成启动动作 JSON** | 把程序/脚本/命令变成可导入 Quicker 的「运行程序或打开文件」动作 |
| 🖼️ **Excel 导出（含真实图标）** | 「图标」列嵌入真实图标图片，离线可用，并自动压缩重复图片媒体 |
| 📦 **批量导出图标文件** | 一次导出全部动作图标为独立 PNG（去重 + 并发 + 本地缓存优先），附 `icons_manifest.json` |

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

### 生成「运行程序或打开文件」动作 JSON（可导入 Quicker）

把任意程序、脚本或命令，直接变成 Quicker 的 **运行程序或打开文件**（ActionType 11）动作定义 JSON，复制内容到面板空白格右键 → 粘贴动作即可导入。

特性与默认值：

| 项 | 默认 | 说明 |
|---|---|---|
| 动作类型 | ActionType 11 | 运行程序或打开文件 |
| 管理员身份 | 否（`RunAsAdmin=false`） | `--admin` 可开启 |
| 已在运行则激活窗口 | 是（`ActivateWindowIfRunning=true`） | `--no-activate` 关闭 |
| 窗口风格 | 最小化（`WindowStyle=2`） | `--no-minimized` 改常规窗口 |
| 工作目录 | 脚本/程序所在目录 | `--workdir` 覆盖 |
| 名称 | 智能生成（脚本 docstring 首行 / 文件名清洗） | `--name` 覆盖 |
| 解释器（.py） | 自动探测能 `import` 其依赖的**最高版本** Python | `--interpreter` 强制指定 |
| 启动方式 | 脚本类（.py/.ps1/.bat/.cmd）默认**脱离 Quicker 启动** | `--no-detach` 改直接启动 |
| 日志重定向 | 关闭 | `--log` 开启，输出到 `.cache/logs/<脚本名>.log`（已被 `.gitignore` 忽略，不进 Git） |

命令示例：

```bash
# 运行 Python 脚本并开启日志（推荐用于后台常驻脚本，便于排查）
python scripts/gen_run_action.py --script "G:\Projects\Tools\potplayer-helper\potplayer_clip.py" --log

# 直接运行/打开程序或文件
python scripts/gen_run_action.py --command "notepad.exe" "C:\a.txt"

# 运行 PowerShell 脚本 / 批处理
python scripts/gen_run_action.py --script "x.ps1"
python scripts/gen_run_action.py --script "x.bat"

# 自定义：名称、工作目录、关闭日志、指定解释器、输出文件
python scripts/gen_run_action.py --script a.py --name "我的动作" --workdir D:\work --no-log --interpreter "C:\Python312\python.exe" --out out.json
```

**为什么要「脱离启动」**：Quicker 的「运行程序或打开文件」会把启动的进程当成自己的子进程跟踪，动作保持「运行中」；依赖全局键盘钩子（如 `keyboard` 库）的脚本会因此收不到按键，直到手动终止动作才生效。脚本类默认通过启动器脱离 Quicker 独立运行——生成器顺带写一个 `.ps1` 启动器到 `.cache/launchers/`（已被 `.gitignore` 忽略），Quicker 动作只执行 `powershell.exe -NoProfile -ExecutionPolicy Bypass -File "<launcher>.ps1"`（与已验证可用的参考动作同构），启动器内部用 `Start-Process` 让目标进程完全脱离，动作立即结束、进程真正后台常驻。

> ⚠️ 不要用 `cmd.exe /c` + `start` 方案：Quicker 启动 cmd 时会接管 stdout 管道，`start` 在管道环境下会等待子进程，整条链被拖住、动作卡在「运行中」（实测踩坑）。`powershell.exe -File` + `Start-Process` 在同样的管道环境下会立即退出，已验证。

日志重定向的实现：开启 `--log` 时，启动器内部用 `Start-Process -RedirectStandardOutput / -RedirectStandardError` 落盘，stdout 写 `.cache/logs/<脚本名>.log`、stderr 写 `<脚本名>.err.log`；导入后可随时打开日志确认执行状态与报错。

> 日志与启动器文件名固定为**纯 ASCII**（取脚本文件名，如 `potplayer_clip.log`，中文自动转下划线）：外壳双层引号里含中文/空格会破坏路径/重定向解析导致文件无法创建；动作标题仍保留智能中文名。日志与启动器均落在 `.cache/` 下，`.gitignore` 已忽略 `*.log` / `logs/` / `.cache/`，不会进入 Git。

### 导出 Excel（含真实图标）

把动作列表导出为 `.xlsx`，**「图标」列写入真实图标图片**（非文字）：

```bash
# 命令行（读取 config.json 的 csv_path）
python scripts/export_actions_excel.py -o quicker_actions.xlsx --size 48

# 注意：需用带依赖的解释器运行，本机为：
# C:\Users\Administrator\.workbuddy\binaries\python\envs\default\Scripts\python.exe
```

```python
connector = QuickerConnector(source="csv")
stats = connector.export_to_excel("quicker_actions.xlsx", icon_size=48)
# => {"total": 357, "with_icon": 350, "no_icon": 7, "output": "...", "resolver_stats": {...}}
```

### 批量导出图标文件

把每个动作的图标导出为**独立 PNG 文件**（去重 + 并发 + 本地缓存优先），并生成清单 `icons_manifest.json`：

```bash
# 命令行（读取 config.json 的 csv_path）
python scripts/icon_exporter.py --out ./icons --size 48 --workers 8
python scripts/icon_exporter.py --out ./icons --no-manifest      # 不生成清单
```

```python
connector = QuickerConnector(source="csv")
stats = connector.export_icons("./icons", size=48, max_workers=8)
# => {"total": 357, "unique": 239, "files": 350, "from_cache": 238, "downloaded": 0,
#     "rendered": 0, "local": 0, "missing": 1, "elapsed_sec": 1.9, "out_dir": "...",
#     "resolver_stats": {...}, "items": [...]}
```

产出：

| 产物 | 说明 |
|---|---|
| `<三位序号>_<动作名>_<图标短key>.png` | 每个动作一个图标文件，动作名已去除 Windows 非法字符并截断到 40 字符 |
| `icons_manifest.json` | `[{id, name, icon, icon_file, source, ok}, ...]`，`source` 为 `url_cache`/`url_download`/`fa_cache`/`fa_render`/`local_file`/`miss` |

### Excel 的三种图标模式（`icon_mode`）

| icon_mode | 「图标」列内容 | Excel 体积 | 适用场景 |
|---|---|---|---|
| `embedded`（默认） | 嵌入真实 PNG 图片（同一 PNG 只存一份媒体） | 中等（本机 357 动作 ≈ 627.5 KB） | 需要直接看到图标 |
| `path` | 只写图标文件的**相对路径** | 很小（≈ 65.5 KB） | 图标另存为文件、Excel 只做索引 |
| `none` | 不处理图标 | 最小（≈ 62 KB） | 只要数据 |

```bash
# 嵌图（默认，先批量导出图标文件到 --icons-dir，再生成 Excel）
python scripts/export_actions_excel.py -o actions.xlsx --icon-mode embedded --icons-dir actions_icons

# 只写路径（Excel 极小，图标按行对应 icons 目录）
python scripts/export_actions_excel.py -o actions.xlsx --icon-mode path --icons-dir actions_icons

# 只要图标文件，不生成 Excel
python scripts/export_actions_excel.py -o actions.xlsx --icons-only --icons-dir actions_icons

# 不处理图标
python scripts/export_actions_excel.py -o actions.xlsx --icon-mode none

# 关闭图片媒体去重（体积 ≈903.3 KB，媒体条目回到 350，与去重版功能等价，仅用于排查/对比）
python scripts/export_actions_excel.py -o actions.xlsx --icon-mode embedded --no-dedupe
```

```python
connector.export_to_excel("actions.xlsx", icon_mode="path", icons_dir="actions_icons")
connector.export_to_excel("actions.xlsx", icon_mode="embedded")   # 默认，等价旧行为
```

### 性能说明（本机实测：357 个动作 / 350 个图标）

| 场景 | 图标解析耗时 | 端到端耗时 | 产物 |
|---|---|---|---|
| 冷缓存（空 `.cache/icons`，含 96 个 FA 渲染 + 最多 4 个联网下载） | ≈1.0–1.5 s | Excel ≈2.6–2.9 s / 图标导出 ≈3.0–3.6 s | ≈627.5 KB |
| 热缓存（239 个唯一图标全部命中本地缓存） | ≈0.03–0.10 s | Excel ≈1.1–1.4 s / 图标导出 ≈1.9–2.1 s | ≈627.5 KB |
| `--icon-mode path` | — | ≈2 s（Excel 生成本身 < 0.3 s） | ≈65.5 KB |
| `--no-dedupe`（关闭媒体压缩） | 同 embedded | 同 embedded | ≈903.3 KB |

> 耗时为本机参考值，随磁盘 IO 与网络状况波动。
> 体积/媒体数与缓存来源无关：冷缓存（4 个 URL 图标联网下载）与热缓存（0 下载）两种状态实测均为 ≈627.5 KB（媒体 350 → 232）。232 是 350 个图标文件中**不同二进制内容**的个数（238 个唯一图标取值中有 6 对产生了字节相同的 PNG），属确定性结果。

优化点：
- **去重**：357 个动作只有 239 个唯一图标取值，同一图标只解析/渲染/下载一次（`resolver_stats.reused = 118`）
- **本地缓存优先**：URL 图标优先命中 Quicker 本地 `ImageCache`（离线），命中即返回，完全不进线程池
- **真并发**：只有需要下载/渲染的取值才走 `ThreadPoolExecutor`（默认 8 线程，仅标准库）
- **媒体压缩**：`embedded` 模式下同一 PNG 在 xlsx 内只保留一份媒体（350 → 232，xlsx ≈627.5 KB；不去重则 ≈903.3 KB）
- **可关闭**：`--no-dedupe` 关闭媒体压缩（媒体条目回到 350、体积 ≈903.3 KB），与去重版功能完全等价，仅用于排查/对比
- **参数校验**：`--size` 必须为 ≥ 1 的整数（如 `--size 0` 会明确报错退出，不会静默产出 0 个图标）

**图标解析规则**（对应 CSV「图标」列的三种取值）：

| 图标取值 | 处理方式 |
|---|---|
| `https://...png` 等图片 URL | 优先命中 Quicker 本地缓存 `%LOCALAPPDATA%\Quicker\ImageCache\<SHA1(完整URL)大写>.png`（**完全离线**）；未命中再联网下载并缓存到 `.cache/icons/url/` |
| `https://...svg`（SVG 图标） | Quicker 缓存/下载后，用内置 SVG 栅格化器渲染成 PNG |
| `fa:Style_Name[:#AARRGGBB]`（字体图标） | 读取 Quicker 自带 `FontAwesomeIconsWpf.dll` 的 SVG 路径数据（已预提取为 `data/fontawesome5_svg_index.json.gz`，5996 个图标，覆盖 Solid/Regular/Light/Brands），纯 Python 栅格化渲染；`#AARRGGBB` 为可选颜色 |
| 空值 / 本地图片路径 | 留空 / 直接使用 |

依赖：`openpyxl`、`Pillow`（渲染无需 pythonnet / 网络）。

相关文件：
- `scripts/export_actions_excel.py` —— Excel 生成（表头样式、冻结窗格、筛选、行高自适应图标、三种 icon_mode、xlsx 媒体去重）
- `scripts/icon_exporter.py` —— 批量导出图标为独立 PNG + `icons_manifest.json`（去重 + 并发 + CLI）
- `scripts/icon_resolver.py` —— 图标取值 → 本地 PNG；`resolve()` 单条 + `resolve_many()` 批量并发
- `scripts/svg_raster.py` —— SVG path / SVG 文件 → PNG 纯 Python 栅格化（even-odd 填充、贝塞尔/圆弧、抗锯齿）
- `scripts/fa_icons.py` —— FontAwesome5 图标数据访问层
- `scripts/build_fa_index.py` —— 从 `FontAwesomeIconsWpf.dll` 重建全量索引（需 pythonnet，一次性）

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

## 🛠️ 数据维护（备份导出映射）

### 全量导出的路径（用户操作指导）

Quicker 的完整配置可以通过维护工具一键导出为**纯文本 JSON 文件**（不需要逐条手动复制）：

1. 打开 Quicker → 点击设置（齿轮）→ **维护工具**
2. 点击 **备份数据 → 备份全部数据**
3. 选择输出目录（本机为 `G:\Data\Tools\Quicker\export`）

官方文档：<https://getquicker.net/KC/Manual/Doc/settings-BasicToolsSettingPage>

该功能会：
- 备份 `quicker.db` 并移除访问密码
- **将所有动作页和动作拆开分别放入单独文件**（这正是本技能数据维护的基础）

### 导出目录结构（映射）

`export_root` 下的文件类型与对应 Quicker 功能，完整机器可读映射见技能知识库：

```
export_root\
├── actionpage_<ID>.json              # 动作页（面板）布局
├── actions\action_<ID>_<名>.json     # 每个动作的完整定义（Data 为 JSON 字符串）
├── states\state_<ID>.json            # 动作状态变量快照
├── states\_action_adorn.json         # 动作徽标/角标/右键菜单装饰
├── common_exe_<程序>.json            # 按程序的轮盘/手势/按键增强/组合键监听
├── common_exe__global.json           # 全局公共触发配置（轮盘/手势/按键）
├── common_shared_subprogram_<ID>.json # 共享子程序
├── common_user_settings.json         # 全局设置（快捷键/触发/定时任务/WebSocket 等）
├── common_user_gestures.json         # 手势预设形状
├── common_user_mouseActions.json     # 鼠标动作
├── common_user_powerKeys.json        # PowerKeys 按键增强
├── common_user_preferences.json      # 界面偏好
└── common_user_favorBlocks.json      # 收藏步骤模块
```

### 使用映射定位与读写配置

技能知识库中的 `data/quicker_export_map.json` 提供「功能 → 文件 → 字段」三级映射。
`scripts/quicker_connector.py` 的 `QuickerExportMap` 类实现代码直接读取与修改：

```python
from quicker_connector import QuickerExportMap

qm = QuickerExportMap()  # 默认读 data/quicker_export_map.json + config.json 的 export_root

# 1. 定位：某个配置在哪个文件哪个字段
info = qm.locate("扩展热键")
# => {"feature": "...", "file": "settings", "json_path": "HotKeysData.ActionHotkeys[]", ...}

# 2. 读取当前值
hotkeys = qm.read_config("扩展热键")

# 3. 修改并写回（自动备份原文件为 .bak）
qm.update_config("左键增强", new_left_button_plus_actions)

# 4. 动作相关
action = qm.find_action("视频旋转修复版")   # 按名称或 ID 定位 actions\ 文件
data = qm.read_action_data("767bc646-b61f-46ce-818f-0b89f38d40d5")  # 解析 Data JSON
```

修改 `actions\*.json` 的 `Data`（动作步骤/变量）属高风险操作，修改前会生成 `.bak` 备份；
Quicker 正在运行时不会热加载这些文件，需通过 Quicker 的「导入动作」或重启后生效。

### 常见配置速查

| 功能 | 文件 | 字段 |
|---|---|---|
| 扩展热键 / 全局快捷键 | `common_user_settings.json` | `HotKeysData`（JSON 字符串） |
| 轮盘菜单动作 | `common_exe_<程序>.json` | `CircleMenuActions` |
| 轮盘开关 | `common_user_settings.json` | `EnableCircleMenu` 等 |
| 手势绑定 | `common_exe_<程序>.json` | `GestureActions` |
| 左键增强（组合键） | `common_user_settings.json` | `LeftButtonPlusActions` |
| 按键连击/长按 | `common_exe_<程序>.json` | `KeyActionItems` |
| 组合键监听 | `common_exe_<程序>.json` | `HotkeyWatcherItems` |
| PowerKeys | `common_user_powerKeys.json` | 整个文件 |
| 定时任务 | `common_user_settings.json` | `AutoRunTaskList` / `TriggerTasks` |
| WebSocket 服务 | `common_user_settings.json` | `WebsocketServerSettings` |

按键格式为 `"修饰码|虚拟键码"`（如 `"2|65"` = Ctrl+A）；动作 `Data` 为 JSON 字符串需二次解析；
映射文件与清单的完整版见 `data/quicker_export_map.json` 和用户侧《Quicker配置映射清单.md》。

## 🔄 导回（导入）能力

### 核心原则：限制导入影响范围

用户修改配置后需要导回 Quicker 时，先判断该配置**能否单文件导回**：

- **能单文件导回的** → 只导回该文件，不影响其它配置
- **不能单文件导回的**（设置类）→ 引导走批量分享导入，且只勾选最小必要数据

注意前提：`export` 目录只是备份快照，**Quicker 运行时不读它**，修改后必须通过下方导入通道生效。

### 决策表（按修改的文件类型）

| 修改的文件 | 导入模式 | 导入方法 |
|---|---|---|
| `actions\action_*.json`（动作） | **single** | 将 JSON 复制到剪贴板，面板空白格右键 → 粘贴动作；或动作右键 → 信息 → 导入动作定义（文件/剪贴板） |
| `states\state_*.json` / `_action_adorn.json` | **single** | 动作右键 → 信息 → 动作数据 → 从云端恢复（仅该动作） |
| `common_shared_subprogram_*.json` | **single** | 子程序管理 → 导入子程序文件（.qka） |
| `actionpage_*.json`（动作页） | **batch** | 批量分享 → 导入动作页数据，只勾选该动作页 |
| `common_user_settings.json`（快捷键/轮盘参数/文本指令/定时任务等） | **batch** | 批量分享 → 导入常规数据（覆盖式） |
| `common_exe_*.json`（按程序的轮盘/手势/按键增强） | **batch** | 批量分享 → 导入常规数据（覆盖式） |
| `common_user_gestures/mouseActions/powerKeys/preferences/favorBlocks.json` | **batch** | 批量分享 → 导入常规数据（覆盖式） |

完整对应关系已写入映射（`data/quicker_export_map.json` 每项的 `import_mode` / `import_method`）。

### 批量导入流程（必须先导出再导入）

1. **先导出、保住现状**：设置 → 维护工具 → 备份数据（全量备份到 export 目录）；或先用批量分享把当前数据分享给自己留底
2. 打开批量分享的导入链接（或自己分享给自己后打开）
3. 只勾选必要数据：常规数据（个人设置/手势/轮盘等）按需勾选；动作页只勾本次涉及的
4. **不要勾选"清空本地数据"**（否则删除本账号所有现有设置）
5. 导入后核对改动生效、其它设置未受影响；异常时用第 1 步备份恢复

> 官方说明：批量导入常规数据时，同账号已有设置会被**覆盖**，所以必须先导出再导入。

### 代码入口（按修改内容自动判断）

```python
qm = QuickerExportMap()
plan = qm.get_import_plan(["扩展热键"])                      # 功能关键词 → batch（设置类）
plan = qm.get_import_plan(["actions\\action_5479d192-...json"])  # 文件 → single（动作）
plan = qm.get_import_plan(["视频旋转修复版"])                 # 动作名 → single
# => {"mode": "single"|"batch", "plans": [...], "steps": [...], "impact": "...", "warning": "..."}
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
