---
name: salary-market-analysis
version: 3.0.0
description: 薪酬市场调研分析技能（全球版）。支持国内+海外多源数据、28字段全球化模板、多币种自动换算（20+货币）、PPP购买力平价调整、分位值计算、17+章节专业报告、外派薪酬建议、多格式输出。
tags: [hr, compensation, salary, benchmarking, market-analysis, report, data-processing, 薪酬调研, 海外薪酬, global-compensation, ppp]
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":{"SALARY_DATA_DIR":"optional - 数据存放目录，默认 skill 目录"}}}}
---

# 薪酬市场调研分析 (Salary Market Analysis) v3.0

专业的薪酬市场调研工具，支持**国内 + 海外**多源数据融合、多币种自动换算、PPP 购买力平价调整、数据清洗、分位值计算和专业报告生成。

---

## ✨ 功能特性

- **28 字段全球化模板**：覆盖基础信息、岗位、公司、薪酬、地域、人才要求 6 大维度
- **多币种自动换算**：支持 20+ 货币（USD/EUR/GBP/JPY/SGD/HKD 等），自动识别国家→货币映射
- **PPP 购买力平价调整**：基于国别薪酬系数矩阵 v2.0，覆盖 27 个国家/地区
- **年薪自动计算**：月薪 × 薪月数，含奖金月份
- **细粒度分位值**：P10/P25/P30/P40/P50/P60/P70/P75/P80/P90，支持加权计算
- **多源数据融合**：国内（BOSS/猎聘/脉脉）+ 海外（LinkedIn/Glassdoor/BLS/ONS）
- **17+ 章节专业报告**：含海外薪酬对比矩阵、PPP 解读、外派薪酬建议
- **外派薪酬计算**：COLA 生活成本调整 + hardship allowance 艰苦补贴
- **多格式输出**：Excel 数据表 + Markdown 报告 + Word 文档

---

## 📁 技能结构

```
skill-salary-market-analysis/
├── SKILL.md                           # 本文件（配置和说明）
├── assets/
│   ├── salary_data_template.csv       # 20 字段基础模板（含 country/currency）
│   └── salary_data_template_24.csv    # 28 字段增强模板 ⭐（含 PPP）
├── references/                        # 参考文档
│   ├── report-template.md             # 17+ 章节报告模板（含海外章节）
│   ├── salary-methodology.md          # 薪酬方法论
│   ├── global-data-sources.md         # 40+ 数据渠道（国内 + 海外）⭐
│   └── data-collection-guide.md       # 数据收集操作指南
└── scripts/                           # Python 脚本
    ├── multi_source_processor.py      # ⭐ 核心处理脚本 V3（多币种 + PPP）
    ├── currency_converter.py          # ⭐ 汇率 + PPP 转换器（独立工具）
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
岗位识别（级别 / 行业 / 地域 / 国家）
  ↓
数据收集（7 种方案可选）
  ├─ 方案 1: 全网搜索 + 手动收集（最稳定，推荐首选）
  ├─ 方案 2: Tampermonkey 用户脚本
  ├─ 方案 3: Chrome 扩展
  ├─ 方案 4: OCR 截图识别
  ├─ 方案 5: Playwright 自动化
  ├─ 方案 6: 海外招聘平台（LinkedIn/Indeed/Glassdoor）
  └─ 方案 7: 政府统计数据（BLS/ONS/MOM）
  ↓
数据处理
  ├─ 多源整合（multi_source_processor.py）
  ├─ 币种自动换算（--target-currency CNY/USD）
  ├─ PPP 购买力平价调整（--with-ppp）
  ├─ 权重应用
  └─ 分位值计算（P10-P90）
  ↓
报告生成
  ├─ Markdown 报告（参照 report-template.md）
  ├─ 海外薪酬对比矩阵
  ├─ 外派薪酬建议
  ├─ Word 格式转换
  └─ Excel 数据输出
```

---

## 📊 28 字段数据模板（全球化增强版）

| # | 字段 | 说明 | 示例 |
|---|------|------|------|
| 1 | id | 唯一标识 | 1 |
| 2 | source | 数据来源 | 前程无忧 / 猎聘 / LinkedIn / Glassdoor / BLS |
| 3 | link | 数据链接 | https://... |
| 4 | collect_date | 收集日期 | 2026-04 |
| 5 | position | 岗位名称 | HR Manager / HRBP |
| 6 | level | 岗位级别 | 总监 / 经理 / 高级 / 初级 |
| 7 | department | 所属部门 | 人力资源部 |
| 8 | responsibility | 职责描述 | 负责... |
| 9 | skills | 技能要求 | SHRM 认证 / 英语流利 |
| 10 | location | 工作地点 | 深圳 / 新加坡 / 旧金山 |
| 11 | country | 国家/地区 | 中国 / 新加坡 / 美国 ⭐ |
| 12 | currency | 原始货币 | CNY / SGD / USD ⭐ |
| 13 | company_name | 公司名称 | DIDA Holdings |
| 14 | company_size | 公司规模 | 1000-5000 人 |
| 15 | industry | 所属行业 | 互联网 / 旅游 |
| 16 | company_type | 公司类型 | 上市公司 / 民营 / 外商独资 |
| 17 | company_address | 公司地址 | 深圳市... |
| 18 | salary_range | 薪酬区间（原始文本） | 4-5.5 万·14 薪 / $120k-150k |
| 19 | salary_structure | 薪酬结构 | 基本工资 + 绩效 + 年终奖 / Base + RSU |
| 20 | benefits | 福利待遇 | 五险一金 / 补充医疗 / 401k |
| 21 | education | 学历要求 | 本科 / 硕士 |
| 22 | major | 专业要求 | 人力资源管理 / 工商管理 |
| 23 | experience | 经验要求 | 5-10 年 |
| 24 | age | 年龄要求 | 30-40 |
| 25 | other_requirements | 其他要求 | 英语六级 / 海外经验 |
| 26 | post_date | 发布日期 | 2026-03-15 |
| 27 | annual_salary_usd | 美元年薪（自动计算）⭐ | 8.5 |
| 28 | ppp_adjusted | PPP 调整后年薪（CNY）⭐ | 22.5 |

### 20 字段基础模板（快速版）

`salary_data_template.csv` 适用于快速调研，包含核心字段 + 海外必需字段：
`id, position, company_name, company_type, salary_range, salary_monthly_low, salary_monthly_high, months, annual_salary_low, annual_salary_high, annual_salary_avg, location, country, currency, annual_salary_usd, ppp_adjusted, experience, education, source, collect_date`

### 年薪计算规则

- 月薪 × 薪月数 ÷ 10000 = 年薪（万元）
- 年薪下限 = 月薪下限 × 薪月数 ÷ 10000
- 年薪上限 = 月薪上限 × 薪月数 ÷ 10000
- 年薪平均 = (年薪下限 + 年薪上限) ÷ 2
- 如标注"X 万/年"则直接取该值

### 海外薪酬口径说明

- **美国**：Base Salary + Bonus + RSU（股票）= Total Compensation
- **新加坡**：13th month AWS + Performance Bonus
- **英国**：Basic + Car Allowance + Pension
- **日本**：基本工资 + 赏与（通常 2 次/年）
- **海外数据填写时务必标注 country 和 currency 字段**

---

## 📈 多源数据整合权重

```python
SOURCE_TYPES = {
    '招聘网站': {'weight': 1.0, 'quality': 0.9},      # BOSS、猎聘、LinkedIn、Indeed 等
    '行业报告': {'weight': 1.2, 'quality': 0.95},      # Mercer、Robert Half、Michael Page
    '财报':     {'weight': 1.1, 'quality': 0.95},      # SEC 10-K、上市公司年报
    '论坛':     {'weight': 0.8, 'quality': 0.7},       # 脉脉、Blind、Reddit 等
    '其他':     {'weight': 0.9, 'quality': 0.75}       # 政府统计等
}
```

---

## 🌍 海外薪酬分析功能

### 汇率换算

内置 25+ 货币汇率表（基准 2026-05），支持通过 CNY 中间货币自动换算：

```bash
# 单笔换算
python3 scripts/currency_converter.py --convert 120000 --from USD --to CNY
# 💱 120000.0 USD = 864000.00 CNY

# CSV 批量换算
python3 scripts/currency_converter.py -i data.csv -o output.csv --target-currency USD
```

### PPP 购买力平价调整

基于国别薪酬系数矩阵 v2.0（27 国），反映同等生活水平需要的薪酬：

```bash
# 单笔 PPP 对比
python3 scripts/currency_converter.py --ppp-salary 1000000 --from-country US --to-country CN
# 📊 PPP 购买力对比：
#    美国: ¥1,000,000 (系数 2.58)
#    ≈ 中国: ¥387,597 (系数 1.00)
#    同等生活水平
```

### 外派薪酬包计算

```bash
# 外派薪酬建议
python3 scripts/currency_converter.py --expat-salary 500000 --host-country SG --home-country CN
# 🌍 外派薪酬包建议 (新加坡):
#    基准薪酬: ¥500,000
#    COLA 调整: +¥525,000 (指数 2.1)
#    艰苦补贴: ¥25,000 (5%)
#    ─────────────
#    总包: ¥1,050,000
```

### 全局分析

```bash
# 海外薪酬分析（自动换算到 USD + PPP 调整）
python3 scripts/multi_source_processor.py -i data.csv -o report.json \
  --target-currency USD --with-ppp --ppp-base-country 中国
```

---

## 📝 参考文档

1. **report-template.md** — 17+ 章节专业报告模板（含海外薪酬章节、外派建议）
2. **salary-methodology.md** — 薪酬调研方法论（分位值定义、PPP 原理）
3. **global-data-sources.md** — 40+ 数据渠道指南（国内 + 海外、政府统计）
4. **data-collection-guide.md** — 数据收集操作指南

---

## 💡 使用示例

### 快速开始

```bash
# 1. 复制 28 字段增强模板
cp assets/salary_data_template_24.csv data.csv

# 2. 收集数据（手动或通过工具）
# ... 填写 data.csv ...

# 3. 数据清洗
python3 scripts/data_cleaner.py -i data.csv -o clean_data.csv

# 4. 国内薪酬分析（默认 CNY）
python3 scripts/multi_source_processor.py -i clean_data.csv -o report.json

# 5. 海外薪酬分析（自动换算到 USD）
python3 scripts/multi_source_processor.py -i clean_data.csv -o report.json --target-currency USD

# 6. PPP 购买力平价调整
python3 scripts/multi_source_processor.py -i clean_data.csv -o report.json --with-ppp

# 7. 转 Excel
python3 scripts/csv_to_excel.py -i clean_data.csv -o salary_report.xlsx
```

### 完整流程（AI 辅助）

1. 用户提供岗位需求（岗位名称 + 地域/国家 + 级别）
2. 使用 `web-search-plus` 搜索目标岗位薪酬信息
3. 提取关键数据填写到 28 字段 CSV 模板
4. 运行清洗和处理脚本
5. 基于报告模板生成 17+ 章节 Markdown 报告
6. 可选转换为 Word 文档

---

## ⚠️ 注意事项

1. **真实数据优先**：明确禁止使用模拟数据，强制从真实渠道获取
2. **数据时效性**：优先收集近 6 个月内的数据
3. **地域差异**：不同城市/国家薪酬差异大，需按地域分类分析
4. **行业对标**：选择同行业或相近行业的数据进行比较
5. **职级匹配**：确保职级定义一致（不同公司职级体系不同）
6. **样本量要求**：每个岗位至少 10 个有效样本，推荐 20+
7. **异常值处理**：极高薪酬（>200 万/年）需标注可能含股权激励
8. **薪月数注意**：注意区分 12 薪、13 薪、14 薪等不同薪月数
9. **海外薪酬口径**：区分 Base Salary / Bonus / RSU / Total Compensation
10. **货币换算**：汇率基准日为 2026-05，实际使用请标注日期
11. **PPP 调整**：购买力平价系数基于 Numbeo/IMF 数据，仅供参考
12. **外派补贴**：COLA + hardship allowance 需结合公司政策调整
