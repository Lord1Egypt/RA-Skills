---
name: system-data-intelligence
description: >
  专为文件操作、数据分析、可视化、数据库连接、API 接入和敏感数据处理设计的系统级 Agent Skill。

  【强制触发场景】：
  - 用户提及任何文件操作：Excel / WPS / Word / TXT / Markdown / RTZ / CSV / JSON
  - 「分析」「读取」「提取」「处理」「建模」「预测」「异常检测」
  - 「生成图表」「可视化」「做仪表盘」「出报告」
  - 「连数据库」「查 SQL」「查 MySQL / PostgreSQL」
  - 「调 API」「从接口拉数据」「爬接口」
  - 「脱敏」「敏感数据」「隐私处理」「数据安全」

  【核心能力】：文件操作（自动降级）× 深度分析 × 专业可视化 × 数据库 × API × 安全脱敏

  IMPORTANT: 只要涉及上述任一场景，必须使用此 skill，不得因"任务简单"而跳过。
---

# System Data Intelligence Skill

## 🔍 快速决策树

**收到任务，先走此树定路径，再执行对应节点的代码：**

```
用户任务
  ├─ 有文件需要读取？
  │    ├─ Windows  → [WIN-PATH]
  │    ├─ macOS    → [MAC-PATH]
  │    └─ Linux    → [LINUX-PATH]
  │
  ├─ 需要查数据库？  → [DB-PATH]
  ├─ 需要调 API？   → [API-PATH]
  ├─ 含敏感数据？   → [SECURITY-PATH]  ← 先执行，再做其他
  ├─ 需要分析数据？ → [ANALYSIS-PATH]
  └─ 需要出图表？   → [VIZ-PATH]
```

**组合任务执行顺序（最常见）：**

```
敏感检测 → 读文件/拉数据 → 分析 → 可视化 → 输出报告
```

---

## [WIN-PATH] Windows 文件读取

**自动降级链：** `win32com` → `openpyxl`（Excel） / `python-docx`（Word）

```python
# 统一入口，自动选策略
from scripts.doc_parser import detect_and_load
data = detect_and_load("report.xlsx")   # 自动 win32com → openpyxl 降级

# 或指定平台脚本
# python scripts/win_excel_reader.py report.xlsx [sheet_name]
# python scripts/wps_extractor.py data.et
```

**WPS 专属 COM 名称：**

| 应用 | COM 名称 |
|---|---|
| WPS 表格（.et） | `KET.Application` |
| WPS 文字（.wps） | `KWPS.Application` |

**注意：** COM 操作结束后必须调用 `Quit()`，已封装到 `safe_com_session` 上下文管理器中。

> 完整手册 → [references/windows-api.md](references/windows-api.md)

---

## [MAC-PATH] macOS 文件读取

**自动降级链：** `xlwings` → `openpyxl`（Excel） / `python-docx`（Word）

```python
# 统一入口，自动选策略
from scripts.doc_parser import detect_and_load
data = detect_and_load("report.xlsx")   # 自动 xlwings → openpyxl 降级

# 或指定平台脚本
# python scripts/mac_excel_reader.py report.xlsx [sheet_name]
```

**权限问题（首次运行必看）：**

```
系统设置 → 隐私与安全性 → 辅助功能 → 开启"终端"或"Python"权限
系统设置 → 隐私与安全性 → 自动化 → 允许控制"Microsoft Excel"
```

> 完整手册 → [references/macos-api.md](references/macos-api.md)

---

## [LINUX-PATH] Linux 文件读取

**策略：** 无 COM/AppleScript，全部用纯 Python 库解析，老格式先用 LibreOffice 转换。

```python
# 统一入口
from scripts.doc_parser import detect_and_load
data = detect_and_load("report.xlsx")   # 直接 openpyxl

# 老格式先转换
# libreoffice --headless --convert-to xlsx input.xls --outdir /tmp/
# libreoffice --headless --convert-to docx input.doc --outdir /tmp/
```

**无头服务器可视化（必须设置）：**

```python
import matplotlib
matplotlib.use('Agg')   # 放在所有 import matplotlib.pyplot 之前
```

**中文字体安装：**

```bash
sudo apt install fonts-noto-cjk && fc-cache -fv
```

> 完整手册 → [references/linux-api.md](references/linux-api.md)

---

## [DB-PATH] 数据库查询

```python
from scripts.db_connector import DBConnector

db = DBConnector("mysql+pymysql://user:pass@host:3306/mydb")

# 普通查询 → DataFrame
df = db.query("SELECT * FROM orders WHERE status = :s", params={"s": "paid"})

# 大表分块（避免 OOM）
for chunk in db.query_chunked("SELECT * FROM logs", chunk_size=10000):
    process(chunk)

db.close()
```

**连接 URL 速查：**

| 数据库 | URL 格式 |
|---|---|
| SQLite | `sqlite:///data.db` |
| MySQL | `mysql+pymysql://user:pass@host:3306/db` |
| PostgreSQL | `postgresql+psycopg2://user:pass@host:5432/db` |
| SQL Server | `mssql+pymssql://user:pass@host:1433/db` |

**CLI 用法：**

```bash
python scripts/db_connector.py "sqlite:///data.db" "SELECT * FROM users" -o result.csv
```

---

## [API-PATH] REST API 数据接入

```python
from scripts.api_loader import APILoader

api = APILoader(base_url="https://api.example.com", timeout=30, max_retries=3)
api.set_auth_token("your_token")   # 或 api.set_api_key("key")

# 单次请求
df = api.fetch_json_to_df("/users", data_key="results")

# 分页自动合并
df = api.fetch_paginated("/items", page_param="page", per_page=100, data_key="data")

# CSV 接口
df = api.fetch_csv_to_df("https://data.example.com/export.csv")

api.close()
```

**CLI 用法：**

```bash
python scripts/api_loader.py "https://api.example.com/data" \
  --data-key results --output data.csv
```

**重试策略：** 默认 3 次，指数退避（1s → 2s → 4s），网络超时、5xx 均触发重试。

---

## [SECURITY-PATH] 敏感数据处理

> **原则：检测到敏感数据，先脱敏再分析，任务结束后清理临时文件。**

```python
from scripts.security_utils import secure_context

with secure_context() as ctx:
    df = load_data(filepath)

    # Step 1: 扫描（返回 {列名: [命中规则]}）
    findings = ctx.masker.detect_sensitive(df)

    # Step 2: 脱敏（仅处理文本列，不破坏结构）
    df_safe = ctx.masker.mask_dataframe(df)

    # Step 3: 安全临时目录（退出自动删除）
    tmp = ctx.cleanup.create_temp_dir()
    df_safe.to_csv(tmp / "safe_data.csv", index=False)

# with 块退出后：临时文件自动删除，内存自动 gc
```

**脱敏效果：**

| 规则 | 原始 | 脱敏后 |
|---|---|---|
| 手机号 | `13812345678` | `138****5678` |
| 身份证 | `110101199001011234` | `110101********1234` |
| 邮箱 | `test@example.com` | `t***@example.com` |
| 银行卡 | `6222021234567890` | `6222 **** **** 7890` |
| IP | `192.168.1.100` | `192.168.*.*` |

---

## [ANALYSIS-PATH] 数据深度分析

**分析层次：**

```
Level 1: 描述性 → 数据现状（均值 / 中位数 / 缺失率 / 分布）
Level 2: 诊断性 → 根因探查（相关性 / 异常检测 / 重复行）
Level 3: 预测性 → 趋势建模（滚动均值 / 环比同比 / 季节性）
Level 4: 规范性 → 决策支持（优化建议 / 洞察摘要）
```

**执行：**

```python
from scripts.deep_analyzer import DeepAnalyzer
import pandas as pd

df = pd.DataFrame(data['sheets']['Sheet1'])   # 来自 detect_and_load
report = DeepAnalyzer(df).run_full_analysis()

# report 结构：
# {
#   'overview':       { shape, columns, dtypes, memory_mb }
#   'quality':        { missing_rate, duplicate_rows, completeness }
#   'distributions':  { col: { mean, median, std, min, max, q25, q75, skewness } }
#   'correlations':   { full_matrix, strong_correlations }
#   'anomalies':      { col: { outlier_count, outlier_pct } }
#   'insights':       [ "...", "..." ]   ← 文字洞察列表
# }
```

**时间序列分析（可选）：**

```python
from scripts.deep_analyzer import analyze_time_series

ts = analyze_time_series(df, date_col="date", value_col="revenue")
# 返回：period / trend_7d / trend_30d / mom_latest / yoy_latest / seasonality_strength
```

**CLI 用法：**

```bash
python scripts/deep_analyzer.py sales.xlsx date revenue
# 输出：outputs/analysis_result.json + outputs/summary.md
```

> 分析参考 → [references/viz-patterns.md](references/viz-patterns.md)

---

## [VIZ-PATH] 数据可视化

**图表选型：**

```
数据特征
  ├─ 时间序列     → 折线图 / 面积图        → create_dashboard()
  ├─ 类别对比     → 柱状图 / 雷达图        → create_radar()
  ├─ 层级占比     → 树状图 / 旭日图        → create_treemap()
  ├─ 流量转化     → 桑基图 / 漏斗图        → create_sankey() / create_funnel()
  ├─ 相关分布     → 散点图 / 热力图        → create_dashboard()
  ├─ 节点关系     → 网络图               → create_network_graph()
  └─ 地理分布     → 散点地图 / 填色地图   → create_geo_map() / create_choropleth()
```

**执行：**

```python
from scripts.viz_engine import (
    create_dashboard, create_network_graph, create_geo_map,
    create_choropleth, create_sankey, create_radar,
    create_treemap, create_funnel, export_viz,
)

# 综合仪表盘（接受 DeepAnalyzer 的 report）
fig = create_dashboard(report, title="销售数据仪表盘")
export_viz(fig, "outputs/report", formats=["html", "png"])

# 网络关系图
fig = create_network_graph(
    edges=[("总部", "上海"), ("总部", "北京"), ("上海", "客户A")],
    title="业务关系图",
)

# 地理散点图
fig = create_geo_map(df, lat_col="lat", lon_col="lon",
                     value_col="sales", label_col="city")
```

**CLI 用法：**

```bash
python scripts/viz_engine.py outputs/analysis_result.json outputs/
# 生成：outputs/report_YYYYMMDD_HHMMSS.html + .png
```

> 图表样式规范 → [references/viz-patterns.md](references/viz-patterns.md)

---

## ⚡ 统一文件入口

**不知道用哪个脚本？永远从这里开始：**

```python
from scripts.doc_parser import detect_and_load

data = detect_and_load("/path/to/any/file", chunk_size=10000, timeout=120)
# 自动做：OS 检测 → 策略选择 → 失败降级 → 大文件分块 → 返回标准化 dict

# data 结构：
# {
#   'type':      'spreadsheet' | 'document' | 'text' | 'json' | 'project'
#   'sheets':    { sheet_name: [[row], [row], ...] }   # 表格类
#   'content':   "..."                                  # 文本类
#   '_file':     "filename.xlsx"
#   '_os':       'Darwin' | 'Windows' | 'Linux'
#   '_strategy': 'openpyxl' | 'win32com' | 'xlwings'   # 实际使用策略
# }
```

**支持格式：** `.xlsx` `.xls` `.xlsm` `.et` `.docx` `.doc` `.wps` `.txt` `.md` `.rtz` `.csv` `.json`

---

## 📤 输出规范

**每次任务完成，必须输出以下四项：**

| 输出 | 路径 | 说明 |
|---|---|---|
| 交互报告 | `outputs/report_YYYYMMDD_HHMMSS.html` | Plotly，可在浏览器操作 |
| 静态图 | `outputs/report_YYYYMMDD_HHMMSS.png` | 高清，适合嵌入文档 |
| 结构化数据 | `outputs/analysis_result.json` | 供后续脚本使用 |
| 洞察摘要 | `outputs/summary.md` | ≤5 行关键结论 |

---

## 💡 执行心法

> **直接行动，不问格式。** 用户说"分析一下"，就给他完整的数据故事：解析→分析→可视化→报告，一气呵成。
>
> **遇到错误不停止。** 首选策略失败 → 自动降级 → 记录日志 → 继续任务。告知用户"使用了备选方案"即可。
>
> **安全优先。** 发现手机号、身份证等敏感字段 → 先脱敏 → 再分析 → 临时文件用 `secure_context` 自动清理。
