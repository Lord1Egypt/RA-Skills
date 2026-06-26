---
name: "xuanself-realtime"
version: "3.0.0"
description: "俄罗斯血糖检测设备市场调研（即时版）v3.0 —— 基于实战经验重构，整合 Python 脚本化报告生成 + SerpAPI 实时搜索 + ast.literal_eval 智能解析 + Xuanself 10章节标准结构，输出可直接交付的 Word 报告。专为 Russia Country Manager 设计，可规避 Error 10004（Token 溢出）问题。"
categories:
  - research
  - market-intelligence
  - medical-device
  - multilingual
  - report-generation
  - russia-market
emoji: "🩸"
author: "WorkBuddy Custom"
homepage: "https://github.com/workbuddy/xuanself-realtime"
metadata:
  openclaw:
    requires:
      bins: ["python3", "pip3"]
    install:
      - id: python-deps
        kind: exec
        command: "pip3 install requests beautifulsoup4 lxml python-docx"
        label: "安装Python依赖"
      - id: serpapi
        kind: note
        text: "SerpAPI Key 配置于本技能 data/data_sources.json（必填，首次使用请替换占位符）"
---

# 俄罗斯血糖检测设备市场调研（即时版）v3.0

## 概述

本技能是 **2026年4月9日实战验证版**（v3.0），整合了多次生产环境调试中积累的核心经验，专门解决：
1. **Error 10004（Token 溢出）**—— 通过 Python 脚本化生成绕过 AI 响应截断
2. **JSON 解析失败**—— `ast.literal_eval()` 智能兜底，处理 Python dict repr 格式
3. **实时数据采集**—— SerpAPI 俄/英双引擎并发搜索
4. **专业 Word 交付**—— Xuanself 标准 10 章节排版

> **典型场景**：Russia Country Manager 需要当天生成一份俄罗斯血糖检测设备（血糖仪/试纸）市场调研报告，实时数据，专业排版，可直接提交。

---

## 核心架构

```
数据采集（SerpAPI / web_fetch）
    ↓
JSON 原始数据（xuanself_raw_YYYYMMDDHHMM.json）
    ↓
data_parser.py（ast.literal_eval 兜底解析）
    ↓
report_generator.py（10章节 Markdown 生成）
    ↓
Word 导出（word_exporter.py v2）
    ↓
交付报告（.docx）
```

---

## 技术要点（实战经验，必须遵守）

### 1. Python 脚本化生成（规避 Error 10004）

**问题**：AI 响应被 token 截断 → Error 10004（"完成原因错误，请重试"）

**解决方案**：将报告生成逻辑写入 Python 脚本文件，执行脚本输出结果：

```python
# 步骤1：用 write_to_file 工具写脚本（不通过 AI 直接输出）
# 步骤2：执行脚本 python your_script.py
# 步骤3：读取输出文件获取报告
```

**核心原则**：
- 永远不要让 AI 直接输出大段报告内容（超过 ~5000 token 会触发截断）
- 将所有逻辑封装为 Python 脚本，通过 `execute_command` 执行
- 数据采集和报告生成分离，JSON 数据落地后再生成报告

### 2. JSON 解析（ast.literal_eval 兜底）

**问题**：SerpAPI 采集的 JSON 中，部分字段（如 `market`）是 Python dict 的 `repr()` 输出（单引号），不是标准 JSON（双引号），`json.loads()` 直接失败。

**解决方案**（已在 `data_parser.py` 中实现）：

```python
import ast, json

def sj(s):
    """智能解析：优先 JSON，兜底 ast.literal_eval"""
    if not s or s.strip() in ("None", "[]", "{}"):
        return None
    try:
        return json.loads(s)         # 标准 JSON
    except:
        pass
    try:
        return ast.literal_eval(s)   # Python repr 格式（单引号）兜底
    except:
        return None
```

**触发条件**：SerpAPI 采集的原始 JSON 中出现单引号 dict（如 `{'key': 'value'}`）时，必须使用此函数。

### 3. BOM 处理（UTF-8-BOM）

**问题**：`write_to_file` 工具写入的文件带 UTF-8-BOM 头（`\xef\xbb\xbf`），Python 执行时报语法错误。

**解决方案**：

```python
def clean_bom(fp):
    """执行前清理 BOM"""
    with open(fp, 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xef\xbb\xbf'):
        with open(fp, 'wb') as f:
            f.write(raw[3:])

clean_bom(script_path)
```

### 4. f-string 冲突处理

**问题**：Python 脚本中的 `{{}}` 在写入时可能被 AI 错误转义。

**解决方案**：在 Python 脚本中使用 `.format()` 方法替代 f-string，避免 `{{}}` 转义问题。

```python
# 错误示例（AI 可能转义）
name = f"Report for {category}"

# 安全示例
name = "Report for {}".format(category)

# 字典格式字符串
"| {} | {} |".format(field1, field2)
```

---

## 数据源矩阵

| 维度 | 数据来源 | 语言 | 优先级 | 数据类型 |
|:---|:---|:---:|:---:|:---|
| 患者数据 | IDF Diabetes Atlas (diabetesatlas.org) | EN | ⭐⭐⭐ | 俄罗斯糖尿病患者统计 |
| 市场规模 | IMEDA、公开财报、SerpAPI 搜索 | RU/EN | ⭐⭐⭐ | TAM/SAM/SOM 估算 |
| 竞争数据 | SerpAPI（Yandex + Google）| RU/EN | ⭐⭐⭐ | TOP品牌、价格区间 |
| 电商价格 | Яндекс.Маркет、Wildberries、Ozon | RU | ⭐⭐⭐ | 实时价格/评分/评论 |
| 行业新闻 | Vademecum.ru、Коммерсантъ、РБК | RU | ⭐⭐⭐ | 2026年实时 |
| 政府政策 | Минздрав、ФФОМС、ГИСП | RU | ⭐⭐⭐ | 报销/进口替代/招标 |
| 社媒情报 | VKontakte、Telegram（SerpAPI 搜索）| RU | ⭐⭐ | 患者社群/品牌口碑 |
| 学术进展 | 俄罗斯内分泌学会（РАЭ）、НМИЦ | RU | ⭐⭐ | SMBG 指南更新 |
| 招标数据 | ЕИС zakupki.gov.ru | RU | ⭐⭐ | 政府中标记录 |

**搜索工具**：SerpAPI（Key 配置于 `data/data_sources.json`），Yandex 和 Google 并发搜索。

---

## 报告结构（Xuanself 标准 10 章节）

```
一、执行摘要
二、市场容量与规模
三、竞争格局分析
四、渠道与价格分析
五、患者群体数据（★必填章节）
六、医学研究进展（★必填章节）
七、政府机构动态与政策（★必填章节）
八、电商平台深度分析
九、招标与采购数据
十、市场进入建议
```

### 必填章节说明

| 章节 | 内容要求 | 数据时效 |
|:---|:---|:---|
| **五、患者群体数据** | IDF 权威统计、1型/2型占比、发病率/死亡率、目标患者细分 | 最新可用年份 |
| **六、医学研究进展** | 临床指南更新（РАЭ 2024-2025）、SMBG 最新研究结论、学术推广平台 | 近12个月 |
| **七、政府动态** | 医保报销政策（ОМС/ЖНВЛП）、进口替代政策（Постановление №1029）、政府采购 | 2026年实时 |

---

## 工作流程

### Phase 1：并行数据采集（使用 SerpAPI）

```python
# 并发搜索俄语 + 英语关键词
queries = [
    # 市场数据
    "рынок глюкометров Россия 2024 2025 объём",
    "blood glucose meter Russia market size TAM SAM",
    # 竞品
    "глюкометр Accu-Chek OneTouch Контур Сателлит Омелон цена",
    "glucometer Russia competitor brand market share 2025",
    # 电商价格
    "глюкометр купить Яндекс.Маркет Wildberries Ozon цена",
    # 患者数据
    "диабет Россия статистика IDF 2024 2025 количество пациентов",
    # 新闻/政策
    "минздрав диабет программа лечение 2025 2026",
    "ОМС глюкометр возмещение Россия 2025",
    # 社媒
    "site:vk.com глюкометр диабет отзывы",
    "site:t.me диабет глюкометр",
]
```

### Phase 2：数据解析与 JSON 落地

```python
from data_parser import smart_json, SmartData

raw = smart_json(raw_json_string)       # 自动处理单引号 dict
ecom = raw.get_list("ecommerce")        # 电商列表
market = raw.get_dict("market")         # 市场规模
vk = raw.get_list("vk")                 # VK 数据
tg = raw.get_list("telegram")           # Telegram 数据
```

### Phase 3：报告生成

```bash
# 进入技能目录
cd ~/.workbuddy/skills/xuanself-realtime

# 生成报告（使用已有数据或新采集数据）
python scripts/run_report.py \
    --input your_raw_data.json \
    --output glucose_report_2026.md \
    --category "血糖检测设备" \
    --country "俄罗斯联邦"

# 导出 Word
python scripts/run_report.py \
    --input glucose_report_2026.md \
    --export-docx glucose_report_2026.docx
```

### Phase 4：Word 导出（v2 排版）

自动使用 `word_exporter.py v2`，标准包括：
- ✅ 封面键值对（`**：**` 和 `**：**` 两种格式）正确解析
- ✅ 内联格式保留（**加粗**、*斜体*、`等宽`、超链接）
- ✅ 表格斑马纹 + 深蓝表头
- ✅ 章节自动分页
- ✅ 页眉（标题+日期）+ 页脚（机密声明）

---

## 关键提示与陷阱

### ⚠️ Error 10004（Token 溢出）
- **不要**让 AI 直接输出大段报告内容
- 始终通过 Python 脚本 + 文件落地方式处理
- 脚本通过 `execute_command` 执行，读取输出文件获取结果

### ⚠️ JSON 单引号解析失败
- SerpAPI 采集的 `market` 等字段可能是 Python repr 格式
- 必须使用 `data_parser.smart_json()` 解析，不可用 `json.loads()` 直接解析

### ⚠️ BOM 导致语法错误
- `write_to_file` 工具写入的脚本带 BOM
- 执行前必须调用 `clean_bom()` 函数清理

### ⚠️ SerpAPI 未被调用
- 某些搜索模块可能绕过 SerpAPI，直接调用 fake-useragent
- 表现：搜索结果质量差，内容不相关
- **确保**：所有搜索统一走 SerpAPI

### ⚠️ 数据时效要求
- 行业新闻/政策：**当天实时**（2026年4月报告：必须为2026年4月数据）
- 患者统计：**最新可用年份**（IDF Atlas 2025 截止2024年统计）
- 电商价格：**近30天内**

---

## 文件结构

```
xuanself-realtime/
├── SKILL.md              ← 主说明文件（本文档）
├── README.md             ← 快速启动指南
├── skill.json            ← Clawhub 标准配置
├── MANIFEST.json         ← 发布清单
├── icon.png              ← 技能图标（可选）
├── requirements.txt      ← Python 依赖
├── scripts/
│   ├── data_parser.py    ← 数据解析核心（ast.literal_eval 兜底）
│   ├── report_generator.py  ← 报告生成器（10章节 Markdown）
│   ├── run_report.py     ← 快捷执行入口
│   └── word_exporter.py ← Word 导出器 v2
├── data/
│   └── data_sources.json ← API Key + 数据源索引
└── output/               ← 报告输出目录
```

---

## 依赖说明

- **Python 依赖**：`requests`, `beautifulsoup4`, `lxml`, `python-docx`
- **外部 API**：SerpAPI（必需，Key 配置于 `data/data_sources.json`）
- **本技能完全自包含**，无需额外安装 report-gama

---

## 更新日志

### v3.0.0（2026-04-09）
- **实战验证版**：基于 2026-04-09 生产环境调试经验重构
- 引入 Python 脚本化报告生成，彻底规避 Error 10004
- `data_parser.py`：`ast.literal_eval()` 智能兜底解析（处理 Python repr 格式）
- `BOM` 清理机制内置于解析器
- `.format()` 方法替代 f-string，避免 `{{}}` 转义问题
- Xuanself 10章节标准结构（3个必填章节）
- 实战验证：成功生成 16.2KB Markdown + 48.6KB Word 报告

### v2.0.0（2026-04-08）
- 13维度报告框架（后来简化为10章节）
- SerpAPI Key 迁移至本技能内置

### v1.0.0（2026-04-05）
- 初始版本

---

*俄罗斯血糖检测设备市场调研（即时版）v3.0.0 — 2026年4月9日 | 实战验证版*
