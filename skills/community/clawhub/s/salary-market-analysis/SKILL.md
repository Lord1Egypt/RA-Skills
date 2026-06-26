---
name: salary-market-analysis
version: 2.0.0
description: 薪酬市场调研分析技能（增强版）。支持多源数据收集、24字段标准化CSV模板、年薪自动计算、分位值计算（P10-P90）、17章节专业报告生成、多格式输出（Excel/Markdown/Word）。
tags: [hr, compensation, salary, benchmarking, market-analysis, report, data-processing, 薪酬调研]
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":{"SALARY_DATA_DIR":"optional - 数据存放目录，默认 skill 目录"}}}}
---

# 薪酬市场调研分析 (Salary Market Analysis)

专业的薪酬市场调研工具，支持多源数据融合、数据清洗、分位值计算和专业报告生成。

---

## ✨ 功能特性

- **24 字段标准化模板**：覆盖基础信息、岗位信息、公司信息、薪酬信息、人才要求 5 大维度
- **年薪自动计算**：月薪 × 薪月数，含奖金月份
- **细粒度分位值**：P10/P25/P30/P40/P50/P60/P70/P75/P80/P90，支持加权计算
- **多源数据融合**：招聘网站 + 行业报告 + 财报 + 论坛，权重可调
- **17 章节专业报告**：从数据概述到调整建议，结构完整
- **多格式输出**：Excel 数据表 + Markdown 报告 + Word 文档

---

## 📁 技能结构

```
skill-salary-market-analysis/
├── SKILL.md                           # 本文件（配置和说明）
├── assets/
│   ├── salary_data_template.csv       # 16 字段基础模板
│   └── salary_data_template_24.csv    # 24 字段增强模板 ⭐
├── references/                        # 参考文档
│   ├── report-template.md             # 17 章节报告模板
│   ├── salary-methodology.md          # 薪酬方法论
│   ├── global-data-sources.md         # 全网数据源指南（20+ 渠道）
│   └── data-collection-guide.md       # 数据收集操作指南
└── scripts/                           # Python 脚本
    ├── multi_source_processor.py      # ⭐ 核心处理脚本（多源整合）
    ├── data_processor.py              # 基础处理器
    ├── data_cleaner.py                # 数据清洗
    ├── csv_to_excel.py                # CSV 转 Excel
    └── markdown_to_word.py            # Markdown 转 Word
```

---

## 🔧 依赖安装

```bash
pip install numpy>=1.21.0 pandas>=1.3.0 openpyxl>=3.0.0 python-docx>=0.8.11 beautifulsoup4>=4.11.0
# 可选：Playwright 自动化
pip install playwright>=1.40.0
playwright install chromium
```

---

## 🔄 工作流程

```
用户需求
  ↓
岗位识别（级别 / 行业 / 地域）
  ↓
数据收集（5 种方案可选）
  ├─ 方案 1: 全网搜索 + 手动收集（最稳定，推荐首选）
  ├─ 方案 2: Tampermonkey 用户脚本
  ├─ 方案 3: Chrome 扩展
  ├─ 方案 4: OCR 截图识别
  └─ 方案 5: Playwright 自动化
  ↓
数据处理
  ├─ 多源整合（multi_source_processor.py）
  ├─ 权重应用
  ├─ 薪酬区间转换（月薪 × 12）
  └─ 分位值计算（P10-P90）
  ↓
报告生成
  ├─ Markdown 报告（参照 report-template.md）
  ├─ Word 格式转换
  └─ Excel 数据输出
```

---

## 📊 24 字段数据模板

| # | 字段 | 说明 | 示例 |
|---|------|------|------|
| 1 | id | 唯一标识 | 1 |
| 2 | source | 数据来源 | 前程无忧 / 猎聘 / 智联招聘 / 脉脉 / 行业报告 |
| 3 | link | 数据链接 | https://... |
| 4 | collect_date | 收集日期 | 2026-04 |
| 5 | position | 岗位名称 | 法务总监 |
| 6 | level | 岗位级别 | 总监 / 经理 / 高级 / 初级 |
| 7 | department | 所属部门 | 法务部 |
| 8 | responsibility | 职责描述 | 负责... |
| 9 | skills | 技能要求 | 法律职业资格 / 英语流利 |
| 10 | location | 工作地点 | 深圳光明 |
| 11 | company_name | 公司名称 | 英威腾电气 |
| 12 | company_size | 公司规模 | 1000-5000 人 |
| 13 | industry | 所属行业 | 制造业 |
| 14 | company_type | 公司类型 | 上市公司 / 民营 / 外商独资 |
| 15 | company_address | 公司地址 | 深圳市光明区... |
| 16 | salary_range | 薪酬区间（原始文本） | 4-5.5 万·14 薪 |
| 17 | salary_structure | 薪酬结构 | 基本工资 + 绩效 + 年终奖 |
| 18 | benefits | 福利待遇 | 五险一金 / 补充医疗 / 年假 |
| 19 | education | 学历要求 | 本科 |
| 20 | major | 专业要求 | 法学 |
| 21 | experience | 经验要求 | 5-10 年 |
| 22 | age | 年龄要求 | 30-40 |
| 23 | other_requirements | 其他要求 | 英语六级 / 有海外经验 |
| 24 | post_date | 发布日期 | 2026-03-15 |

### 16 字段模板（快速版）

`salary_data_template.csv` 适用于快速调研，仅包含核心字段：
`id, position, company_name, company_type, salary_range, salary_monthly_low, salary_monthly_high, months, annual_salary_low, annual_salary_high, annual_salary_avg, location, experience, education, source, collect_date`

### 年薪计算规则

- 月薪 × 薪月数 ÷ 10000 = 年薪（万元）
- 年薪下限 = 月薪下限 × 薪月数 ÷ 10000
- 年薪上限 = 月薪上限 × 薪月数 ÷ 10000
- 年薪平均 = (年薪下限 + 年薪上限) ÷ 2
- 如标注"X 万/年"则直接取该值

---

## 📈 多源数据整合权重

```python
SOURCE_TYPES = {
    '招聘网站': {'weight': 1.0, 'quality': 0.9},      # 前程无忧、猎聘、智联招聘等
    '行业报告': {'weight': 1.2, 'quality': 0.95},      # Mercer、Willis Towers Watson
    '财报':     {'weight': 1.1, 'quality': 0.95},      # 上市公司年报
    '论坛':     {'weight': 0.8, 'quality': 0.7},       # 脉脉、知乎等
    '其他':     {'weight': 0.9, 'quality': 0.75}       # 其他来源
}
```

---

## 📝 参考文档

1. **report-template.md** - 17 章节专业报告模板（数据概况、分位值、行业对比、薪酬诊断、调整建议）
2. **salary-methodology.md** - 薪酬调研方法论（分位值定义、统计学原理、数据质量评估）
3. **global-data-sources.md** - 20+ 数据渠道指南（薪酬分享平台、社交媒体、技术社区、行业报告）
4. **data-collection-guide.md** - 数据收集操作指南

---

## 💡 使用示例

### 快速开始

```bash
# 1. 复制 24 字段模板
cp assets/salary_data_template_24.csv data.csv

# 2. 收集数据（手动或通过工具）
# ... 填写 data.csv ...

# 3. 数据清洗
python3 scripts/data_cleaner.py -i data.csv -o clean_data.csv

# 4. 生成报告
python3 scripts/multi_source_processor.py -i clean_data.csv -o report.json

# 5. 转 Excel
python3 scripts/csv_to_excel.py -i clean_data.csv -o salary_report.xlsx
```

### 完整流程（AI 辅助）

1. 用户提供岗位需求（岗位名称 + 地域 + 级别）
2. 使用 `web-search-plus` 搜索目标岗位薪酬信息
3. 提取关键数据填写到 24 字段 CSV 模板
4. 运行清洗和处理脚本
5. 基于报告模板生成 17 章节 Markdown 报告
6. 可选转换为 Word 文档

---

## ⚠️ 注意事项

1. **真实数据优先**：明确禁止使用模拟数据，强制从真实渠道获取
2. **数据时效性**：优先收集近 6 个月内的数据
3. **地域差异**：不同城市薪酬差异大，需按地域分类分析
4. **行业对标**：选择同行业或相近行业的数据进行比较
5. **样本量要求**：每个岗位至少 10 个有效样本，推荐 20+
6. **异常值处理**：极高薪酬（>200 万/年）需标注可能含股权激励
7. **薪月数注意**：注意区分 12 薪、13 薪、14 薪等不同薪月数
