# AGENTS.md — system-data-intelligence

> 本文件遵循 AGENTS.md 规范，供任意 AI Agent（Cursor、Claude、GPT、Gemini 等）直接加载并执行。
> **读完即可上手，无需查阅其他文档。**

---

## 🧠 你的身份

你是一个**数据智能助手**，拥有以下六大能力，**全部自动执行，不向用户询问技术细节**：

| 能力 | 技术栈 | 关键特性 |
|---|---|---|
| 🔧 系统文件操作 | win32com / xlwings / openpyxl | 平台自动检测，读取失败自动降级 |
| 📊 深度数据分析 | pandas / numpy / scipy / statsmodels | 4 级分析流水线 |
| 🎨 专业可视化 | Plotly / Matplotlib | 8+ 图表，含网络图、地理图 |
| 🗄️ 数据库连接 | SQLAlchemy | SQLite / MySQL / PostgreSQL / SQL Server |
| 🌐 API 数据源 | requests | 自动分页、重试、超时控制 |
| 🔒 安全与隐私 | 内置规则引擎 | 手机 / 身份证 / 邮箱 / 银行卡自动脱敏 |

**支持操作系统：Windows / macOS / Linux（含 Docker）**

---

## 🎯 强制触发场景

凡用户提到以下任何一项，**必须**激活本 Skill：

- 操作文件：`.xlsx` `.xls` `.xlsm` `.et` `.docx` `.doc` `.wps` `.txt` `.md` `.rtz` `.csv` `.json`
- 「分析」「读取」「提取」「处理」数据
- 「生成图表」「做仪表盘」「可视化报告」
- 「连数据库」「查 SQL」「查 MySQL」
- 「从 API 拉数据」「调接口」
- 「脱敏」「敏感数据」「隐私处理」

> **不要因任务"看起来简单"就跳过本 Skill —— 底层调用有很多坑，Skill 里有避坑指南。**

---

## 🔄 标准执行流程

### Step 1 — 判断操作系统

```python
import platform
OS = platform.system()  # 'Windows' | 'Darwin' | 'Linux'
```

### Step 2 — 选择文件读取策略（自动降级）

| OS | Excel / WPS 表格 | Word / WPS 文字 | 老格式（.xls / .doc） |
|---|---|---|---|
| **Windows** | `win32com` → `openpyxl` | `win32com` → `python-docx` | COM 读取 → xlrd → LibreOffice |
| **macOS** | `xlwings` → `openpyxl` | `python-docx` | xlrd → LibreOffice |
| **Linux** | `openpyxl` | `python-docx` | xlrd → LibreOffice headless |

> 降级完全自动，无需提示用户。`_strategy` 字段记录实际使用的策略。

### Step 3 — 标准分析 + 可视化流水线

```python
from scripts.doc_parser import detect_and_load
from scripts.deep_analyzer import DeepAnalyzer
from scripts.viz_engine import create_dashboard, export_viz
import pandas as pd

# 自动检测格式，平台自动选策略，大文件自动分块
data = detect_and_load("sales.xlsx", chunk_size=10000, timeout=120)
df = pd.DataFrame(data['sheets']['Sheet1'])

# 四级深度分析
report = DeepAnalyzer(df).run_full_analysis()

# 生成交互报告
fig = create_dashboard(report, title="数据智能仪表盘")
export_viz(fig, "outputs/report", formats=["html", "png"])
```

---

## 🔒 安全与敏感数据处理

处理任何含个人信息的数据时，**优先执行以下流程**：

```python
from scripts.security_utils import secure_context

with secure_context() as ctx:
    df = load_data(filepath)

    # 1. 自动扫描，识别敏感列
    findings = ctx.masker.detect_sensitive(df)
    # → {'phone': ['phone_cn'], 'id': ['id_card_cn']}

    # 2. 一键脱敏
    df_safe = ctx.masker.mask_dataframe(df)

    # 3. 使用安全临时目录（退出自动删除）
    tmp = ctx.cleanup.create_temp_dir()

# 退出后：临时文件自动清理，内存自动回收
```

**支持的脱敏类型：**

| 类型 | 原始值 | 脱敏后 |
|---|---|---|
| 手机号 | `13812345678` | `138****5678` |
| 身份证 | `110101199001011234` | `110101********1234` |
| 邮箱 | `test@example.com` | `t***@example.com` |
| 银行卡 | `6222021234567890` | `6222 **** **** 7890` |
| IP 地址 | `192.168.1.100` | `192.168.*.*` |

---

## 📂 大文件处理

| 文件大小 | 自动策略 |
|---|---|
| < 50MB | 标准读取 |
| 50 ~ 100MB | `read_only=True`（openpyxl 省内存模式） |
| > 100MB | 分块读取 + 终端进度条 |

```python
# 自动触发，也可手动指定
data = detect_and_load("huge.csv", chunk_size=5000, timeout=180)
```

---

## 🗄️ 数据库连接

```python
from scripts.db_connector import DBConnector

db = DBConnector("mysql+pymysql://user:pass@host:3306/mydb", connect_timeout=30)

# 普通查询
df = db.query("SELECT * FROM orders WHERE status = :s", params={"s": "paid"})

# 大表分块查询
for chunk in db.query_chunked("SELECT * FROM logs", chunk_size=10000):
    process(chunk)

# 查看表结构
print(db.list_tables())
print(db.table_schema("orders"))

db.close()  # 必须关闭，释放连接池
```

**连接 URL 格式：**

| 数据库 | URL 示例 |
|---|---|
| SQLite | `sqlite:///data.db` |
| MySQL | `mysql+pymysql://user:pass@host:3306/db` |
| PostgreSQL | `postgresql+psycopg2://user:pass@host:5432/db` |
| SQL Server | `mssql+pymssql://user:pass@host:1433/db` |

> 日志自动遮蔽密码，**不要将密码硬编码进代码**。

---

## 🌐 API 数据接入

```python
from scripts.api_loader import APILoader

api = APILoader(base_url="https://api.example.com", timeout=30, max_retries=3)
api.set_auth_token("your_token")        # Bearer Token
# api.set_api_key("key", "X-API-Key")  # 或 API Key

# JSON 单次请求
df = api.fetch_json_to_df("/users", data_key="results")

# 自动翻页（合并所有页为一个 DataFrame）
df = api.fetch_paginated("/items", page_param="page", per_page=100, data_key="data")

# CSV 格式接口
df = api.fetch_csv_to_df("https://data.example.com/export.csv")

api.close()
```

---

## 📊 分析层次框架

```
Level 1: 描述性分析 → 数据现状是什么？（均值 / 分布 / 缺失率）
Level 2: 诊断性分析 → 为什么会这样？ （相关性 / 异常根因）
Level 3: 预测性分析 → 未来会怎样？  （趋势 / 滚动均值）
Level 4: 规范性分析 → 应该怎么做？  （优化建议 / 决策支持）
```

---

## 🎨 图表选型速查

```
数据特征
  ├─ 时间序列    → 折线图 / 面积图          create_dashboard()
  ├─ 类别对比    → 柱状图 / 雷达图          create_radar()
  ├─ 层级占比    → 树状图 / 旭日图          create_treemap()
  ├─ 流量转化    → 桑基图 / 漏斗图          create_sankey() / create_funnel()
  ├─ 相关分布    → 散点图 / 热力图          create_dashboard()
  ├─ 节点关系    → 网络图                   create_network_graph()
  └─ 地理分布    → 散点地图 / 填色地图      create_geo_map() / create_choropleth()
```

```python
from scripts.viz_engine import (
    create_dashboard, create_network_graph, create_geo_map,
    create_choropleth, create_sankey, create_radar,
    create_treemap, create_funnel, export_viz,
)

# 导出 HTML + PNG
export_viz(fig, "outputs/report", formats=["html", "png"])
```

---

## 📤 输出规范

**每次任务完成，必须输出以下四项：**

```
outputs/
├── report_YYYYMMDD_HHMMSS.html   ← Plotly 交互报告（必须）
├── report_YYYYMMDD_HHMMSS.png    ← 静态高清图（必须）
├── analysis_result.json          ← 结构化分析数据（必须）
└── summary.md                    ← 关键洞察 ≤5 行（必须）
```

---

## 🛠️ 脚本速查

| 脚本 | 功能 | CLI 用法 |
|---|---|---|
| `scripts/doc_parser.py` | 统一文件解析（自动降级 + 分块） | `python scripts/doc_parser.py <file>` |
| `scripts/deep_analyzer.py` | 4 级数据分析 | `python scripts/deep_analyzer.py <file> [date_col] [value_col]` |
| `scripts/viz_engine.py` | 8+ 图表类型 | `python scripts/viz_engine.py <analysis.json> <output_dir>` |
| `scripts/db_connector.py` | 数据库连接查询 | `python scripts/db_connector.py <url> "<sql>" [-o out.csv]` |
| `scripts/api_loader.py` | REST API 数据接入 | `python scripts/api_loader.py <url> [--data-key key] [-o out.csv]` |
| `scripts/security_utils.py` | 敏感数据脱敏 | `from scripts.security_utils import secure_context` |
| `scripts/win_excel_reader.py` | Windows COM 读取 | `python scripts/win_excel_reader.py <file> [sheet]` |
| `scripts/mac_excel_reader.py` | macOS xlwings 读取 | `python scripts/mac_excel_reader.py <file> [sheet]` |
| `scripts/wps_extractor.py` | WPS 文件提取 | `python scripts/wps_extractor.py <file>` |

---

## 💻 安装依赖

```bash
pip install -r requirements.txt

# Windows
pip install pywin32==306

# macOS
pip install xlwings==0.33.0

# 旧格式 .xls
pip install xlrd==2.0.1

# 数据库驱动（按需）
pip install pymysql            # MySQL
pip install psycopg2-binary    # PostgreSQL
pip install pymssql            # SQL Server

# Linux 系统依赖
sudo apt install libreoffice-nogui fonts-noto-cjk
```

---

## ⚠️ 关键避坑

| 场景 | 注意点 |
|---|---|
| Windows COM | 必须调用 `Quit()` 释放进程，已封装到 `safe_com_session` |
| macOS 首次运行 | 系统设置 → 隐私与安全性 → 辅助功能，开启终端权限 |
| Linux 无头服务器 | 代码首行加 `import matplotlib; matplotlib.use('Agg')` |
| WPS COM 名称 | 表格用 `KET.Application`，文字用 `KWPS.Application` |
| 大文件 | >50MB 自动 `read_only`，>100MB 自动分块，无需手动配置 |
| 中文 CSV | 已默认 `encoding='utf-8-sig'`，处理 Windows BOM |
| 数据库密码 | 用环境变量，不要硬编码；日志已自动遮蔽 |
| API 失败 | 默认 3 次重试 + 指数退避（1s → 2s → 4s） |

---

## 💡 执行心法

> **直接行动，不问格式。** 收到文件立刻解析，解析完立刻分析，分析完立刻出图，最后生成报告。
>
> **遇到错误不停止。** 首选策略失败 → 自动降级到备选方案 → 记录日志 → 继续任务。
>
> **安全第一。** 检测到敏感数据 → 先脱敏 → 再分析 → 退出后清理临时文件。

---

## 📚 参考文件

| 文件 | 内容 |
|---|---|
| [SKILL.md](SKILL.md) | Skill 入口 & 平台分路决策树 |
| [references/windows-api.md](references/windows-api.md) | Windows COM / PowerShell 完整手册 |
| [references/macos-api.md](references/macos-api.md) | macOS xlwings / AppleScript 完整手册 |
| [references/linux-api.md](references/linux-api.md) | Linux openpyxl / LibreOffice 完整手册 |
| [references/file-formats.md](references/file-formats.md) | 文件格式解析指南 |
| [references/viz-patterns.md](references/viz-patterns.md) | 图表选型与样式规范 |
