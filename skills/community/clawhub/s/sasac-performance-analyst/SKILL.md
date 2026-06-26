---
name: sasac-performance-analyst
version: 2.0.0
description: |
  国资委企业绩效评价智能分析SKILL | SASAC Enterprise Performance Evaluation Skill
  基于2025年版《企业绩效评价标准值》，提供精准对标、绩效诊断、改进建议与报告生成。
  覆盖10大行业门类、48个行业中类、107个行业小类、332个标准值表（含国际对标）。
author: 王东杰 (Wang Dongjie)
title: CFO首席财务官 | 资深复合型战略财务专家 | CGMA持证人
email: Wdj_@163.com
license: MIT
language: zh-CN | en-US
tags: 
  - sasac
  - performance-evaluation
  - state-owned-enterprise
  - benchmarking
  - financial-analysis
  - cgma
  - ifrs
  - hkex-ipo
  - enterprise-performance
  - china-soe
repository: https://github.com/yjkj999999/sasac-performance-analyst
clawhub: https://clawhub.ai/yjkj999999/sasac-performance-analyst
homepage: https://github.com/yjkj999999/sasac-performance-analyst#readme
keywords:
  - 国资委
  - 企业绩效评价
  - 标准值
  - 对标分析
  - 绩效评价
  - SASAC
  - SOE
  - performance-benchmarking
  - CGMA
  - financial-accounting
  - hkex-ipo
  - ifrs
  - cas-accounting
  - prospectus-analysis
  - cross-listing
date: 2026-05-17
---

# 国资委企业绩效评价智能分析SKILL (SASAC Performance Analyst v2.0)

> 基于国务院国资委《企业绩效评价标准值（2025）》构建的企业绩效对标评价智能分析系统。
> 助力国有企业打造"世界一流财务管理体系"，服务"新质生产力"与高质量发展。

---

## 系统概述

### 核心能力

| 能力模块 | 描述 |
|---------|------|
| 🔍 **精准对标** | 输入指标数值，自动判定优秀/良好/中等/较低/较差五档位 |
| 📊 **四维诊断** | 盈利回报、资产运营、风险防控、持续发展四维雷达图 |
| 📈 **评分引擎** | 五档线性插值评分，权重配置（盈利30%/运营20%/风险25%/发展25%） |
| 📋 **报告生成** | 综合评价报告，支持多格式输出（HTML/PDF/腾讯文档） |
| 🌍 **国际对标** | 19个行业国际标准值（2024）对标功能 |
| 📄 **招股书解析** | 港交所IPO招股书财务数据自动提取与对标 |
| 🔗 **跨境上市评估** | 国企港股上市可行性评估与绩效差距分析 |

### 数据底座

- **标准值表**：332个（国内314 + 国际18）
- **行业覆盖**：10个行业大类、48个行业中类、107个行业小类
- **指标体系**：24项指标（16项核心 + 8项补充）
- **评价等级**：优秀值、良好值、中等值、较低值、较差值
- **规模分类**：全行业、大型企业、中型企业、小型企业

---

## 快速开始

### 安装

```bash
# 方法1：通过 SkillHub 安装（推荐）
skillon install sasac-performance-analyst

# 方法2：通过 ClawHub 安装
openclaw skills install sasac-performance-analyst

# 方法3：手动安装
git clone https://github.com/yjkj999999/sasac-performance-analyst.git ~/.qclaw/skills/sasac-performance-analyst/
```

### 最小使用示例

```
用户：我是一家大型医药工业企业，2025年净资产收益率15%，研发经费投入强度4%。

AI助手：
📊 【对标结果】
  净资产收益率(15%)：处于【良好值】区间
    （优秀值17.1%，良好值12.7%，差距12%）
  研发经费投入强度(4%)：处于【中等值】区间
    （优秀值7.9%，良好值5.9%，差距49%）

💡 【诊断结论】
  盈利能力良好，但持续发展能力（研发投入）不足，存在"重当期利润、轻长远发展"风险。

📋 【改进建议】
  参考医药工业标杆企业案例，建议：
  1. 将研发投入提升至优秀值（7.9%）以上
  2. 建立研发经费投入强度考核机制
  3. 参考中国中车"创新绩效评价管理"案例
```

---

## 核心模块详解

### 模块一：数据对标引擎

#### 支持的24项指标

**盈利回报维度（4项）**
| 指标 | 单位 | 计算公式 |
|------|------|---------|
| 净资产收益率 | % | 净利润 / 平均净资产 × 100% |
| 营业收入利润率 | % | 营业利润 / 营业总收入 × 100% |
| 总资产报酬率 | % | 息税前利润 / 平均资产总额 × 100% |
| 盈余现金保障倍数 | 倍 | 经营活动现金净流量 / 净利润 |

**资产运营维度（4项）**
| 指标 | 单位 | 计算公式 |
|------|------|---------|
| 总资产周转率 | 次 | 营业总收入 / 平均资产总额 |
| 应收账款周转率 | 次 | 营业总收入 / 平均应收账款余额 |
| 流动资产周转率 | 次 | 营业总收入 / 平均流动资产总额 |
| 两金占流动资产比重 | % | (应收账款+存货) / 流动资产 × 100% |

**风险防控维度（4项）**
| 指标 | 单位 | 计算公式 |
|------|------|---------|
| 资产负债率 | % | 负债总额 / 资产总额 × 100% |
| 现金流动负债比率 | % | 经营活动现金净流量 / 流动负债 × 100% |
| 带息负债比率 | % | 带息负债总额 / 负债总额 × 100% |
| 已获利息倍数 | 倍 | 息税前利润 / 利息支出 |

**持续发展维度（4项）**
| 指标 | 单位 | 计算公式 |
|------|------|---------|
| 研发经费投入强度 | % | 研发经费支出 / 营业总收入 × 100% |
| 全员劳动生产率 | 万元/人 | 劳动生产总值 / 全部从业人员平均人数 |
| 经济增加值率 | % | 经济增加值 / 调整后资本 × 100% |
| 国有资本保值增值率 | % | 期末国有资本权益 / 期初国有资本权益 × 100% |

**补充指标（8项）**
营业现金比率、国有资本回报率、EBITDA率、百元收入支付的成本费用、存货周转率、速动比率、利润总额增长率、营业总收入增长率

#### 五档评分算法

```python
def linear_interpolation(value, benchmark):
    """
    线性插值计算得分
    benchmark: [优秀值, 良好值, 中等值, 较低值, 较差值]
    返回: 得分(0-100)，以及等级描述
    """
    excellent, good, medium, low, poor = benchmark
    
    if value >= excellent:
        return 100, "优秀"
    elif value >= good:
        ratio = (value - good) / (excellent - good)
        return 80 + ratio * 20, "良好+"
    elif value >= medium:
        ratio = (value - medium) / (good - medium)
        return 60 + ratio * 20, "良好"
    elif value >= low:
        ratio = (value - low) / (medium - low)
        return 40 + ratio * 20, "中等"
    elif value >= poor:
        ratio = (value - poor) / (low - poor)
        return 20 + ratio * 20, "较低"
    else:
        return 0, "较差"
```

### 模块二：综合评价引擎

#### 维度权重配置

```python
WEIGHTS = {
    "盈利回报": 0.30,   # 30%
    "资产运营": 0.20,   # 20%
    "风险防控": 0.25,   # 25%
    "持续发展": 0.25,   # 25%
}
```

#### 综合得分计算

```python
def calculate_composite_score(scores, weights=WEIGHTS):
    """计算加权综合得分"""
    total = sum(scores[dim] * weight for dim, weight in weights.items())
    return round(total, 2)
```

#### 评价等级映射

| 综合得分 | 评价等级 |
|---------|---------|
| 85-100 | A+ 卓越 |
| 70-84 | A 优秀 |
| 55-69 | B 良好 |
| 40-54 | C 中等 |
| 25-39 | D 较低 |
| 0-24 | E 较差 |

### 模块三：行业分类映射

#### 证监会行业分类 ↔ 国民经济行业分类 ↔ SASAC分类 映射表

```python
INDUSTRY_MAPPING = {
    # 证监会大类 → SASAC大类
    "农、林、牧、渔业": "农林牧渔业",
    "采矿业": "工业",
    "制造业": "工业",
    "电力、热力、燃气及水生产和供应业": "电力工业 / 水生产和供应业",
    "建筑业": "建筑业",
    "批发和零售业": "批发和零售业",
    "交通运输、仓储和邮政业": "交通运输、仓储及邮政业",
    "住宿和餐饮业": "住宿和餐饮业",
    "信息传输、软件和信息技术服务业": "信息技术服务业",
    "房地产业": "房地产业",
    "租赁和商务服务业": "社会服务业",
    "文化、体育和娱乐业": "文化、体育和娱乐业",
}
```

### 模块四：港股IPO招股书数据集成

#### 数据来源
- **知识库**：IMA「香港上市招股书」（知识库ID: `UEGKn91QubH8gaMsReTGEYZ0qMzWdS-RPYN__3pcKUk=`）
- **覆盖规模**：3,629家港股上市公司（其中已上市1,251家）
- **行业分布**：科技/半导体(145)、生物医药(141)、金融(41)、新能源(17)、消费(16)

#### 招股书解析流程

```python
def parse_prospectus_financial_data(pdf_path):
    """
    从港股IPO招股书提取财务数据
    支持IFRS与CAS准则差异调整
    """
    # 1. 定位财务表格（fitz PDF解析）
    # 2. 识别货币单位（人民币千元 / 港币千元）
    # 3. 提取3年财务数据
    # 4. IFRS → CAS 准则调整
    # 5. 计算24项指标
    # 6. 对标SASAC标准值
    # 7. 生成差距分析报告
```

#### IFRS与CAS准则差异调整

| 项目 | IFRS | CAS | 调整说明 |
|------|------|-----|---------|
| 研发支出 | 费用化为主 | 有条件资本化 | 需加回资本化研发支出 |
| 政府补助 | 冲减相关资产成本 | 单独确认为收益 | 需调整政府补助处理 |
| 公允价值计量 | 更广泛使用 | 更谨慎使用 | 需调整公允价值变动损益 |

---

## 工具函数

### performance_calculator.py

```python
from tools.performance_calculator import (
    evaluate_indicator,      # 单指标对标
    full_diagnosis,          # 全面诊断
    calculate_composite_score, # 综合评分
    linear_interpolation,     # 线性插值
    get_benchmark,           # 获取标准值
    classify_size,           # 企业规模分类
)

# 示例：单指标对标
result = evaluate_indicator(
    industry="医药工业",
    size="大型企业",
    indicator="净资产收益率",
    value=15.0
)
# 返回: {"level": "良好值", "score": 72.5, "gap_to_excellent": "12%"}

# 示例：全面诊断
report = full_diagnosis(
    industry="医药工业",
    size="大型企业",
    data={
        "净资产收益率": 15.0,
        "营业收入利润率": 12.0,
        "总资产报酬率": 8.5,
        # ... 其他22项指标
    }
)
```

### visualization.py

```python
from tools.visualization import (
    generate_radar_chart,    # 雷达图
    generate_bar_chart,      # 柱状图
    generate_trend_chart,    # 趋势图
    generate_full_report,     # 完整报告
)

# 生成雷达图
radar_path = generate_radar_chart(
    scores={"盈利回报": 72.5, "资产运营": 68.0, "风险防控": 55.0, "持续发展": 45.0},
    title="某医药工业企业绩效雷达图",
    output_path="output/radar.png"
)

# 生成完整HTML报告
report_path = generate_full_report(
    report_data=report,
    output_format="html",  # or "pdf"
    output_path="output/report.html"
)
```

### financial_data_extractor.py

```python
from tools.financial_data_extractor import (
    extract_from_pdf,         # 从PDF提取
    extract_from_cninfo,      # 从巨潮网提取
    extract_from_hkex,        # 从港交所提取
)

# 从港股招股书PDF提取
summary = extract_from_pdf(
    pdf_path="/path/to/prospectus.pdf",
    output_path="/path/to/output.json"
)

# 从巨潮网提取（A股上市公司）
data = extract_from_cninfo(
    stock_code="000001.SZ",
    year=2024,
    quarter=4
)
```

### hk_ipo_integration.py

```python
from tools.hk_ipo_integration import (
    get_hk_ipo_integration,     # 获取港股集成数据
    generate_cross_listing_report, # 生成跨境上市报告
    compare_with_listed_peers,   # 与已上市公司对比
)

# 获取行业分布
hk_integration = get_hk_ipo_integration()
industry_dist = hk_integration.get_industry_distribution()

# 生成跨境上市报告
report = generate_cross_listing_report(
    company_name="某国有企业",
    industry="电子工业",
    financial_data={
        "净资产收益率": 15.2,
        "资产负债率": 55.3,
        "研发经费投入强度": 8.5
    }
)
```

---

## 最佳实践案例库

### 核心案例（5家央企）

#### 1. 国家电网 — "智驱·精效"绩效评价体系
- **背景**：建设世界一流企业，需要科学的绩效评价系统
- **方案**：构建"智驱·精效"绩效评价体系，涵盖4维度16项指标
- **成果**：实现精准对标、差异化管理、智能化决策

#### 2. 中国华能 — 分层分类绩效评价体系
- **背景**：多元化业务结构，需要差异化评价标准
- **方案**：按业务板块分层分类，建立多维度评价标准
- **成果**：提升管理精细化水平，激发基层创新活力

#### 3. 中国铝业 — 数智化绩效评价赋能穿透监管
- **背景**：大型矿业企业，监管链条长、难度大
- **方案**：数智化绩效评价体系，实现穿透式监管
- **成果**：提升监管效率，降低经营风险

#### 4. 中国中车 — 创新绩效评价管理打造大国重器
- **背景**：高端装备制造企业，创新驱动发展
- **方案**：将研发投入、创新产出纳入绩效评价体系
- **成果**：激发创新活力，打造世界一流轨道交通装备企业

#### 5. 中国海油 — 覆盖全级次贯通全过程绩效评价
- **背景**：跨国能源企业，组织层级多、业务流程复杂
- **方案**：覆盖全级次、贯通全过程的绩效评价体系
- **成果**：实现全局优化，提升整体运营效率

### 港股上市案例（扩展）

| 行业 | 代表企业 | 对标要点 |
|------|---------|---------|
| 科技/半导体 | 上海曦智科技、勝宏科技 | 研发投入强度对标 |
| 生物医药 | 邁威生物、北京天星醫療 | 营收增长率对标 |
| 新能源 | 思格新能源、瑞浦蘭鈞能源 | EBITDA率对标 |
| 消费 | 牧原食品、海天調味食品 | 毛利率对标 |
| 金融 | 陽光保險、渤海銀行 | ROE对标 |

---

## 文件结构

```
sasac-performance-analyst/
├── SKILL.md                          # 技能定义（本文件）
├── README.md                         # 使用说明（英文）
├── README_ZH.md                     # 使用说明（中文）
├── package.json                     # 技能元数据
├── system_prompt.md                  # 系统提示词（AI角色设定）
├── data/
│   ├── sasac_2025_standards.json   # 2025年标准值（完整332表）
│   ├── international_standards.json # 国际标准值（18表）
│   ├── industry_mapping.json        # 行业分类映射表
│   ├── case_studies.json           # 核心案例（5家）
│   ├── hk_ipo_db.json              # 港股招股书数据库
│   └── cross_listing_db.json       # 跨境上市评估数据库
├── tools/
│   ├── performance_calculator.py    # 绩效计算工具
│   ├── visualization.py             # 可视化工具
│   ├── financial_data_extractor.py # 财务数据提取工具
│   ├── hk_ipo_integration.py       # 港股IPO集成工具
│   └── report_generator.py         # 报告生成工具
├── templates/
│   ├── report_template.html        # 报告HTML模板
│   └── csv_template.csv           # CSV导出模板
├── html/
│   └── sasac_performance_query_2025.html  # 交互式查询系统
└── output/                          # 输出目录（自动生成）
```

---

## API参考

### evaluate_indicator()

```python
def evaluate_indicator(
    industry: str,       # 行业名称（如"医药工业"）
    size: str,           # 规模（"全行业"/"大型企业"/"中型企业"/"小型企业"）
    indicator: str,      # 指标名称（如"净资产收益率"）
    value: float,        # 企业实际值
    standard_year: int = 2025  # 标准值年份
) -> dict:
    """
    单指标对标评估
    
    返回:
    {
        "indicator": "净资产收益率",
        "value": 15.0,
        "benchmark": [17.1, 12.7, 8.5, 3.2, -2.1],
        "level": "良好值",
        "score": 72.5,
        "gap_to_excellent": "12%",
        "gap_to_medium": "76%",
        "suggestion": "建议提升至优秀值(17.1%)以上"
    }
    """
```

### full_diagnosis()

```python
def full_diagnosis(
    industry: str,
    size: str,
    data: dict,          # {指标名: 值} 字典
    standard_year: int = 2025
) -> dict:
    """
    全面绩效诊断
    
    返回:
    {
        "composite_score": 62.3,
        "grade": "B 良好",
        "dimension_scores": {
            "盈利回报": 72.5,
            "资产运营": 68.0,
            "风险防控": 55.0,
            "持续发展": 45.0
        },
        "strengths": ["盈利回报"],
        "weaknesses": ["持续发展"],
        "recommendations": [...],
        "radar_chart_path": "output/radar.png"
    }
    """
```

---

## 版本历史

### v2.0.0 (2026-05-17) — 🎉 重大更新
- ✅ **完整数据**：从10个行业扩展到332个标准值表（314国内+18国际）
- ✅ **国际对标**：新增19个行业国际标准值（2024）对标功能
- ✅ **交互式查询系统**：新增 `html/sasac_performance_query_2025.html`
- ✅ **行业大类筛选**：支持按10大行业门类快速筛选
- ✅ **来源筛选**：区分国内/国际标准值
- ✅ **CSV导出增强**：增加"行业大类"和"来源"列
- ✅ **OCR修复**：修复釆→采、増→增等字符问题
- ✅ **行业分类映射**：新增证监会分类 ↔ SASAC分类映射
- ✅ **评分引擎**：新增五档线性插值评分算法
- ✅ **综合评价**：新增四维加权综合评分（盈利30%/运营20%/风险25%/发展25%）

### v1.2.1 (2025-05-12)
- 成功提取南京英派药业招股书财务数据
- 建立首个香港上市公司财务指标数据库记录
- 验证PDF财务数据提取流程可行性

### v1.2.0 (2025-05-11)
- 新增财务数据提取器
- 新增跨境上市可行性评估模型
- 建立香港上市公司财务指标数据库（3,629家公司）

### v1.1.0 (2025-05-11)
- 集成IMA香港上市招股书知识库
- 新增跨境上市绩效对标服务模块
- 扩展行业映射：科技→电子工业、生物医药→医药工业

### v1.0.0 (2025-05-11)
- 初始版本，包含全国国有企业、工业、煤炭工业基础数据
- 核心功能：精准对标、诊断雷达、管理建议

---

## 许可证

MIT License — 详见 [LICENSE](LICENSE)

## 作者

**王东杰 (Wang Dongjie)**
- 职务：CFO 首席财务官 | 资深复合型战略财务专家
- 资质：CGMA（皇家特许管理会计师）持证人
- 专长：上市公司资本运作、集团化财务管控、企业绩效评价
- 邮箱：Wdj_@163.com
- 电话：13952453499

## 致谢

- 国务院国资委考核分配局（《企业绩效评价标准值2025》数据来源）
- 经济科学出版社（出版单位）
- AICPA & CIMA（CGMA知识体系）
- 香港交易所（IPO招股书数据）

---

## 使用约束

- 必须严格依据2025版标准值数据进行判断，不可凭空捏造数据
- 若用户未提供行业/规模，默认使用"全国国有企业-全行业"标准，并提示用户细化
- 语言风格要专业、客观、具有指导性，体现"世界一流"的标准
- 港股招股书数据仅用于已公开披露的上市公司，遵守相关保密规定

---

**🚀 开始使用：** `skillon install sasac-performance-analyst`
