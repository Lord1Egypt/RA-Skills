# system-data-Intelligence

> 专为 AI Agent 设计的**系统级数据智能 Skill**，支持文件操作、深度分析、专业可视化、数据库连接、API 接入与安全脱敏，全平台自动降级，开箱即用。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)](#-安装)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](#-安装)
[![Tests](https://img.shields.io/badge/tests-pytest-brightgreen)](#-测试)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED)](#-docker-部署)
[![Agent Compatible](https://img.shields.io/badge/AGENTS.md-compatible-purple)](AGENTS.md)

---

## ✨ 六大核心能力

| 能力 | 技术栈 | 亮点 |
|---|---|---|
| 🔧 **系统文件操作** | win32com / xlwings / openpyxl | 平台自动检测，失败自动降级 |
| 📊 **深度数据分析** | pandas / numpy / scipy / statsmodels | 4 级分析：描述→诊断→预测→规范 |
| 🎨 **专业可视化** | Plotly / Matplotlib | 8+ 图表类型，含网络图、地理图 |
| 🗄️ **数据库连接** | SQLAlchemy | SQLite / MySQL / PostgreSQL / SQL Server |
| 🌐 **API 数据源** | requests | 自动分页、重试、超时控制 |
| 🔒 **安全与隐私** | 内置规则引擎 | 手机/身份证/邮箱/银行卡自动脱敏 |

**支持文件格式：** `.xlsx` `.xls` `.xlsm` `.et` `.docx` `.doc` `.wps` `.txt` `.md` `.rtz` `.csv` `.json`

---

## 🤖 AI Agent 接入方式

| Agent | 接入方法 |
|---|---|
| **Cursor** | 复制到 `~/.cursor/skills/system-data-intelligence` 自动加载 |
| **Claude / OpenClaw** | 将 [AGENTS.md](AGENTS.md) 内容作为 System Prompt |
| **GPT / 其他** | 将 [SKILL.md](SKILL.md) 内容粘贴到对话框 |

---

## 📁 项目结构

```
system-data-intelligence/
├── SKILL.md                  ← Agent Skill 入口 & 决策树
├── AGENTS.md                 ← 通用 AI Agent 使用说明
├── Dockerfile                ← Linux Docker 镜像
├── docker-compose.yml        ← 一键启动
├── requirements.txt          ← 锁定版本依赖
├── scripts/
│   ├── doc_parser.py         ← 统一文件解析（自动降级 + 分块）
│   ├── deep_analyzer.py      ← 4 级数据分析引擎
│   ├── viz_engine.py         ← 可视化引擎（8+ 图表）
│   ├── db_connector.py       ← 数据库连接（SQLAlchemy）
│   ├── api_loader.py         ← REST API 数据接入
│   ├── security_utils.py     ← 敏感数据脱敏 & 安全清理
│   ├── win_excel_reader.py   ← Windows COM 读取
│   ├── mac_excel_reader.py   ← macOS xlwings 读取
│   └── wps_extractor.py      ← WPS 格式提取
├── references/
│   ├── windows-api.md        ← Windows COM / PowerShell 手册
│   ├── macos-api.md          ← macOS xlwings / AppleScript 手册
│   ├── linux-api.md          ← Linux openpyxl / LibreOffice 手册
│   ├── file-formats.md       ← 文件格式解析指南
│   └── viz-patterns.md       ← 图表选型指南
└── tests/
    ├── test_doc_parser.py
    ├── test_deep_analyzer.py
    ├── test_viz_engine.py
    ├── test_security_utils.py
    └── test_db_connector.py
```

---

## 🚀 安装

### 基础安装（全平台）

```bash
git clone https://github.com/zhaojie911272507/system-data-Intelligence.git
cd system-data-intelligence
pip install -r requirements.txt
```

### 平台特定依赖

```bash
# Windows
pip install pywin32==306

# macOS
pip install xlwings==0.33.0

# 旧格式 .xls 支持（全平台）
pip install xlrd==2.0.1
```

### 数据库驱动（按需安装）

```bash
pip install pymysql           # MySQL
pip install psycopg2-binary   # PostgreSQL
pip install pymssql           # SQL Server
```

### Linux 系统依赖

```bash
sudo apt install libreoffice-nogui fonts-noto-cjk
```

---

## 💡 快速开始

### 场景一：读取文件并分析

```python
from scripts.doc_parser import detect_and_load
from scripts.deep_analyzer import DeepAnalyzer
from scripts.viz_engine import create_dashboard, export_viz

# 自动识别格式，平台自动降级
data = detect_and_load("sales.xlsx")

import pandas as pd
df = pd.DataFrame(data['sheets']['Sheet1'])

# 四级深度分析
report = DeepAnalyzer(df).run_full_analysis()

# 生成可视化报告
fig = create_dashboard(report, title="销售数据仪表盘")
export_viz(fig, "outputs/report")
```

### 场景二：处理敏感数据

```python
from scripts.security_utils import secure_context

with secure_context() as ctx:
    df = load_data("customers.csv")

    # 自动扫描敏感字段
    findings = ctx.masker.detect_sensitive(df)
    # → {'phone': ['phone_cn'], 'email': ['email']}

    # 一键脱敏
    df_safe = ctx.masker.mask_dataframe(df)
    # 13812345678 → 138****5678

# 退出后自动清理临时文件，释放内存
```

### 场景三：数据库查询

```python
from scripts.db_connector import DBConnector

db = DBConnector("mysql+pymysql://user:pass@host:3306/mydb")
df = db.query("SELECT * FROM orders WHERE year = 2025")

# 大表分块查询
for chunk in db.query_chunked("SELECT * FROM big_table", chunk_size=10000):
    process(chunk)

db.close()
```

### 场景四：API 数据接入

```python
from scripts.api_loader import APILoader

api = APILoader(base_url="https://api.example.com", timeout=30, max_retries=3)
api.set_auth_token("your_token")

# 自动分页翻页并合并
df = api.fetch_paginated("/items", page_param="page", per_page=100, data_key="data")
api.close()
```

---

## 🎨 可视化图表类型

| 图表 | 函数 | 适用场景 |
|---|---|---|
| 综合仪表盘 | `create_dashboard()` | 分析报告总览 |
| 网络关系图 | `create_network_graph()` | 节点关系、社交网络 |
| 地理散点图 | `create_geo_map()` | 经纬度数据 |
| 区域填色图 | `create_choropleth()` | 国家/省份对比 |
| 桑基图 | `create_sankey()` | 流量/转化路径 |
| 雷达图 | `create_radar()` | 多维度对比 |
| 树状图 | `create_treemap()` | 层级占比 |
| 漏斗图 | `create_funnel()` | 转化率分析 |

```python
from scripts.viz_engine import create_network_graph, export_viz

fig = create_network_graph(
    edges=[('总部', '上海'), ('总部', '北京'), ('上海', '客户A')],
    title="业务关系图"
)
export_viz(fig, "outputs/network", formats=["html", "png"])
```

---

## 🔄 自动降级机制

文件读取按平台自动选择最优策略，失败则无缝切换：

```
Windows Excel:  win32com ──→ openpyxl
macOS Excel:    xlwings  ──→ openpyxl
.xls 旧格式:    win32com ──→ xlrd ──→ libreoffice+openpyxl
.doc/.wps 文档: win32com ──→ python-docx
```

---

## 📤 输出规范

每次分析任务自动生成：

```
outputs/
├── report_YYYYMMDD_HHMMSS.html   ← Plotly 交互报告
├── report_YYYYMMDD_HHMMSS.png    ← 静态高清图
├── analysis_result.json          ← 结构化分析数据
└── summary.md                    ← 关键洞察（≤5行）
```

---

## 🐳 Docker 部署

适用于 Linux 服务器环境，无需手动配置依赖：

```bash
docker compose up -d
docker exec -it sdi-app python scripts/doc_parser.py /data/example.xlsx
```

---

## 🧪 测试

```bash
# 运行全部测试
pytest tests/ -v

# 带覆盖率报告
pytest tests/ --cov=scripts --cov-report=html

# 运行单个模块
pytest tests/test_doc_parser.py -v
```

---

## 📚 参考文档

| 文档 | 内容 |
|---|---|
| [AGENTS.md](AGENTS.md) | AI Agent 完整使用规范 |
| [SKILL.md](SKILL.md) | Skill 入口与决策树 |
| [references/windows-api.md](references/windows-api.md) | Windows COM 详细手册 |
| [references/macos-api.md](references/macos-api.md) | macOS xlwings 手册 |
| [references/linux-api.md](references/linux-api.md) | Linux openpyxl 手册 |
| [references/viz-patterns.md](references/viz-patterns.md) | 图表选型指南 |

---

## 📋 Changelog

### v2.0.0 (2026-03-08)
- 新增自动降级 Fallback 机制（`fallback_chain` / `with_retry`）
- 新增 `security_utils.py` — 手机/身份证/邮箱/银行卡脱敏
- 新增 `db_connector.py` — SQLite / MySQL / PostgreSQL / SQL Server
- 新增 `api_loader.py` — REST API 分页接入
- `viz_engine.py` 扩展至 8+ 图表类型（网络图、地理图、桑基图等）
- 新增 `tests/` 单元测试套件
- 新增 Docker 支持
- `requirements.txt` 所有依赖锁定版本

### v1.0.0
- 核心文件解析（Excel / Word / WPS / CSV / JSON / RTZ）
- 4 级数据分析引擎
- Plotly 仪表盘 + Matplotlib 静态导出
- Windows COM / macOS xlwings 支持

---

## 📄 License

MIT License — 自由使用、修改与分发。
