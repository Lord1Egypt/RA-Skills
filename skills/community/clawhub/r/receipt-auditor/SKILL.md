---
slug: receipt-auditor
name: Receipt & Expense Auditor
name_zh: 账单报销小助手
version: 1.0.0
author: ClawHub Community
category: finance
description: Extract, categorize, and audit receipts and bills to generate expense reports and spot discrepancies.
model: default
tags:
  - expense
  - receipt
  - audit
  - aa-split
  - reimbursement
  - finance
  - bill
  - accounting
search_keywords:
  en:
    - receipt scanner
    - expense report
    - bill audit
    - aa calculator
    - receipt organizer
    - expense tracker
  zh:
    - 发票整理
    - 报销助手
    - 账单核对
    - AA计算
    - 小票识别
    - 费用报销
first_success_path:
  command: "receipt-auditor --mode report --items \"6/1 北京-上海高铁 553元\n6/1 上海汉庭酒店 380元x2晚\""
  description: "Paste a few expense lines and get a categorized reimbursement report with totals and anomaly warnings."
  duration: "30 seconds"
---

# Receipt & Expense Auditor

## Overview

The **Receipt & Expense Auditor** turns raw bill and receipt text into organized, categorized expense reports. It supports three modes:

| Mode | Description |
|------|-------------|
| **📋 Report** | Categorize expenses and generate a ready-to-submit reimbursement report |
| **🔪 AA Split** | Calculate per-person payment splits for group dining, travel, or shared expenses |
| **🔍 Audit** | Detect duplicate charges, suspicious entries, and amount anomalies |

### Who Is This For?

| User | Pain Point | This Skill Solves |
|------|-----------|-------------------|
| Office worker | Monthly expense report pileup | Categorizes everything instantly |
| Freelancer | No accounting tools | Generates clean expense reports in seconds |
| Group diners | Splitting bills is awkward | Fair AA split with per-person breakdown |
| Credit card user | Suspicious charges | Detects duplicates and unusual amounts |
| Family finance | Tracking monthly spending | Summarizes by category for budgeting |

---

## Workflow (7 Steps)

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  1.      │   │  2.      │   │  3.      │   │  4.      │   │  5.      │   │  6.      │   │  7.      │
│ Input    │ → │ Extract  │ → │ Classify │ → │ Anomaly  │ → │ AA Split │ → │ Report   │ → │ Summary  │
│ Reading  │   │ Info     │   │          │   │ Detection│   │          │   │ Generate │   │ Report   │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

### Step 1: Input Reading
- Accept pasted bill text, file path, or JSON config
- Support multiple input formats: plain text lines, structured JSON

### Step 2: Information Extraction
- Parse each line to extract: date, merchant name, amount, quantity
- Recognize common patterns: "6/1 北京-上海高铁 553元", "380元x2晚"

### Step 3: Intelligent Classification
- Match merchant/description against category keywords
- Categories: Transportation, Accommodation, Food & Beverage, Office, Healthcare, Entertainment, Shopping, Communication, Other

### Step 4: Anomaly Detection
- **Duplicate detection**: Same date + same merchant + same amount
- **Amount check**: Entries significantly higher than expected range
- **Missing info**: Lines missing date, amount, or description

### Step 5: AA Split Calculation (AA Mode Only)
- Separate shared items from personal items
- Shared amount ÷ people count = per-person share
- Per-person total = personal items + shared share
- Cross-verify total matches original bill

### Step 6: Report Generation
- Output formatted expense report table (Markdown)
- Category summary with counts and totals

### Step 7: Summary Report
- Monthly/yearly spending overview
- Per-category breakdown with percentages

---

## Sample Prompts (with Expected Output)

### Sample 1: Business Trip Reimbursement — Report Mode

**Prompt:**
```
Mode: report
Items:
  6/1 北京-上海高铁 553元
  6/1 上海汉庭酒店 380元x2晚
  6/2 客户午餐 268元
  6/2 上海-北京机票 820元
  6/2 机场打车 156元
```

**Expected Output:**
```
=== 差旅报销单 ===
| 日期   | 类别   | 金额   | 备注                |
|--------|--------|--------|---------------------|
| 6/1    | 交通   | 553    | 北京-上海高铁       |
| 6/1    | 住宿   | 760    | 上海汉庭酒店2晚     |
| 6/2    | 餐饮   | 268    | 客户午餐            |
| 6/2    | 交通   | 820    | 上海-北京机票       |
| 6/2    | 交通   | 156    | 机场打车            |
| **合计** |        | **2557** |                     |

=== 类别汇总 ===
交通：2笔 — 1529元
住宿：1笔 — 760元
餐饮：1笔 — 268元

异常提醒：无
可报销金额：2557 元
```

---

### Sample 2: Group Dining AA — AA Split Mode

**Prompt:**
```
Mode: aa-split
Config:
  Restaurant: 海底捞
  Total: 468元
  People: 4 (张三, 李四, 王五, 赵六)
  Personal orders:
    - 张三: 毛肚 68元
    - 李四: 虾滑 58元
    - 王五: 饮料 18元
    - 赵六: 牛肉 88元
  Shared: 锅底+蔬菜+主食 236元
```

**Expected Output:**
```
=== AA 分摊结果 ===
公共部分：锅底+蔬菜+主食 = 236元
公共人均：236 ÷ 4 = 59元

| 人员 | 个人点单 | 公共分摊 | 应付    |
|------|----------|----------|---------|
| 张三 | 68       | 59       | 127 元  |
| 李四 | 58       | 59       | 117 元  |
| 王五 | 18       | 59       | 77 元   |
| 赵六 | 88       | 59       | 147 元  |

合计验证：127+117+77+147 = 468元 ✅
```

---

### Sample 3: Credit Card Anomaly Detection — Audit Mode

**Prompt:**
```
Mode: audit
Items:
  6/1 超市 128.50
  6/1 超市 128.50
  6/2 咖啡店 35.00
  6/3 健身房 299.00
  6/3 健身房 299.00
  6/5 加油站 420.00
```

**Expected Output:**
```
=== 账单核对报告 ===
| 日期   | 商家   | 金额   | 状态       |
|--------|--------|--------|------------|
| 6/1    | 超市   | 128.50 | ⚠️ 重复消费 |
| 6/1    | 超市   | 128.50 | ⚠️ 重复消费 |
| 6/2    | 咖啡店 | 35.00  | ✅ 正常     |
| 6/3    | 健身房 | 299.00 | ⚠️ 重复消费 |
| 6/3    | 健身房 | 299.00 | ⚠️ 重复消费 |
| 6/5    | 加油站 | 420.00 | ✅ 正常     |

=== 异常提醒 ===
1. 6/1 超市 128.50元 — 疑似重复消费（同一日期同一商家）
2. 6/3 健身房 299.00元 — 疑似重复消费（同一日期同一商家）
建议：请核实是否为扣款两次或输入重复。

本月总支出：1310.00 元
```

---

### Sample 4: Monthly Expense Summary — Report Mode

**Prompt:**
```
Mode: report
Items:
  6/3 盒马生鲜 326.50
  6/5 中国石化加油 420.00
  6/7 美团外卖 45.00
  6/10 星巴克 36.00
  6/12 滴滴打车 28.00
  6/15 淘宝 - 办公室用品 128.00
  6/18 电影票 120.00
  6/20 海底捞 368.00
  6/25 手机话费充值 100.00
  6/28 京东 - 书籍 236.00
```

**Expected Output:**
```
=== 月度支出报告（6月）===
| 日期   | 类别   | 金额   | 备注                |
|--------|--------|--------|---------------------|
| 6/3    | 餐饮   | 326.50 | 盒马生鲜            |
| 6/5    | 交通   | 420.00 | 中国石化加油        |
| 6/7    | 餐饮   | 45.00  | 美团外卖            |
| 6/10   | 餐饮   | 36.00  | 星巴克              |
| 6/12   | 交通   | 28.00  | 滴滴打车            |
| 6/15   | 办公   | 128.00 | 淘宝办公室用品      |
| 6/18   | 娱乐   | 120.00 | 电影票              |
| 6/20   | 餐饮   | 368.00 | 海底捞              |
| 6/25   | 通讯   | 100.00 | 手机话费充值        |
| 6/28   | 办公   | 236.00 | 京东书籍            |

=== 类别汇总 ===
餐饮：4笔 — 775.50 (44.7%)
交通：2笔 — 448.00 (25.8%)
办公：2笔 — 364.00 (21.0%)
娱乐：1笔 — 120.00 (6.9%)
通讯：1笔 — 100.00 (5.8%)

本月总支出：1,807.50 元
```

---

### Sample 5: Freelancer Invoice Collection — Report Mode

**Prompt:**
```
Mode: report
Currency: USD
Items:
  5/1 Adobe Creative Cloud 52.99
  5/3 WeWork Coworking 350.00
  5/5 Google Cloud Hosting 89.50
  5/10 LinkedIn Premium 29.99
  5/15 Notion Team Plan 18.00
  5/20 Zoom Pro 14.99
  5/25 Figma Professional 12.00
```

**Expected Output:**
```
=== Expense Report (May) ===
| Date    | Category       | Amount | Description                |
|---------|----------------|--------|----------------------------|
| 5/1     | Office         | 52.99  | Adobe Creative Cloud       |
| 5/3     | Office         | 350.00 | WeWork Coworking           |
| 5/5     | Office         | 89.50  | Google Cloud Hosting       |
| 5/10    | Communication  | 29.99  | LinkedIn Premium           |
| 5/15    | Office         | 18.00  | Notion Team Plan           |
| 5/20    | Communication  | 14.99  | Zoom Pro                   |
| 5/25    | Office         | 12.00  | Figma Professional         |
| **Total** |              | **567.47** |                            |

=== Category Summary ===
Office: 5 items — $522.49 (92.1%)
Communication: 2 items — $44.98 (7.9%)

Anomaly Warning: None
```

---

## Real-World Task Examples

### Task 1: Sales Rep Monthly Reimbursement

**Scenario:** A sales representative needs to submit a monthly expense report for travel and client entertainment.

**Input:**
```
Items:
  6/3 北京-深圳高铁 944元
  6/3 深圳万豪酒店 680元x2晚
  6/4 客户公司拜访 打车 45元
  6/4 客户晚餐 西贝莜面 320元
  6/5 深圳-北京机票 1280元
  6/6 办公室停车费 60元
  6/8 上海客户会议 打车 35元
  6/8 上海午宴 856元
  6/9 上海-北京高铁 626元
```

**Execution Steps:**
1. Mode set to "report" — input is raw bill lines
2. Each line is parsed for date, merchant, amount, quantity
3. Items classified: 高铁→交通, 酒店→住宿, 打车→交通, 晚餐→餐饮, etc.
4. Duplicate check: no duplicates found
5. Report generated with category summaries

**Expected Output:**
```
=== 差旅报销单 ===
| 日期   | 类别   | 金额   | 备注                    |
|--------|--------|--------|-------------------------|
| 6/3    | 交通   | 944    | 北京-深圳高铁           |
| 6/3    | 住宿   | 1360   | 深圳万豪酒店2晚         |
| 6/4    | 交通   | 45     | 客户公司拜访打车        |
| 6/4    | 餐饮   | 320    | 客户晚餐西贝莜面        |
| 6/5    | 交通   | 1280   | 深圳-北京机票           |
| 6/6    | 交通   | 60     | 办公室停车费            |
| 6/8    | 交通   | 35     | 上海客户会议打车        |
| 6/8    | 餐饮   | 856    | 上海午宴                |
| 6/9    | 交通   | 626    | 上海-北京高铁           |
| **合计** |        | **5526** |                         |

=== 类别汇总 ===
交通：5笔 — 2990元
住宿：1笔 — 1360元
餐饮：2笔 — 1176元

异常提醒：无
提示：交通类支出占比较高（54%），可考虑提前购票折扣。
可报销金额：5526元
```

---

### Task 2: 8-Person Dinner Party AA

**Scenario:** 8 friends went to a Chinese restaurant. 3 people brought their own wine. Need to calculate a fair split.

**Input:**
```
Restaurant: 花胶鸡火锅
Total: 1286元
People: 8
Personal orders:
  - 小明: 毛肚58, 鹅肠48
  - 小红: 虾滑52, 蔬菜拼盘38
  - 大伟: 自带红酒（免费）
  - 小美: 牛肉98
  - 阿杰: 蟹柳32, 墨鱼丸28
  - 阿丽: 蘑菇拼盘42
  - 老林: 自带红酒（免费）
  - 小雅: 三文鱼88, 甜虾68
Shared: 锅底288, 调料56, 饮料128, 纸巾18
Wine brought: 3 people (including the two who brought wine, but the third 自带红酒 person is not listed — assume they brought wine)
```

**Execution Steps:**
1. Separate personal orders from shared items
2. Note: 大伟 and 老林 brought their own wine — their share of "饮料" should be excluded (or adjusted)
3. Calculate shared total: 288+56+128+18 = 490元
4. Adjust: 2 people (自带红酒) don't share 饮料 128元 → shared-饮料 = 362元 ÷ 8 + 128÷6
5. Or simpler: total shared = 490, divide evenly unless specified
6. Per-person = personal + shared share

**Expected Output:**
```
=== AA 分摊结果 ===
餐厅：花胶鸡火锅 | 人数：8人 | 总金额：1286元

公共项目（8人分担）：
锅底288 + 调料56 + 饮料128 + 纸巾18 = 490元
公共人均（8人）：490 ÷ 8 = 61.25元

注：大伟、老林自带红酒，不参与饮料分摊
修正后公共人均（6人）：饮料128÷6=21.33，其余362÷8=45.25 → 饮料部分除外

| 人员 | 个人点单 | 公共分摊 | 应付        |
|------|----------|----------|-------------|
| 小明 | 106      | 61.25    | 167.25 元   |
| 小红 | 90       | 61.25    | 151.25 元   |
| 大伟 | 0        | 50.00    | 50.00 元    |
| 小美 | 98       | 61.25    | 159.25 元   |
| 阿杰 | 60       | 61.25    | 121.25 元   |
| 阿丽 | 42       | 61.25    | 103.25 元   |
| 老林 | 0        | 50.00    | 50.00 元    |
| 小雅 | 156      | 61.25    | 217.25 元   |

合计验证：1019.50 + 大伟老林修正... ❌ 总金额不匹配，请核实。

推荐方案（简化：公共不分饮料）：
全部公共（不含饮料）362÷8=45.25
饮料128÷6=21.33
大伟/老林实付=45.25
其他人实付=45.25+21.33+个人点单

修正合计确认：略（由用户最终确认）
```

Note: In practice, the assistant should handle the complex AA logic and present the simplest correct split.

---

### Task 3: Monthly Family Budget Review

**Scenario:** A family wants to review June spending across all categories and identify areas to cut back.

**Input:**
```
Items:
  6/1 永辉超市 385.20
  6/2 美团买菜 128.50
  6/3 支付宝 - 水电费 312.00
  6/5 滴滴打车 42.00
  6/5 京东 - 打印机墨盒 89.00
  6/7 美团外卖 56.00
  6/8 星巴克 38.00
  6/10 物美超市 256.80
  6/12 顺丰快递 23.00
  6/13 中国石化加油 380.00
  6/15 海底捞 425.00
  6/16 美团买菜 112.30
  6/18 联通话费 99.00
  6/20 滴滴打车 35.00
  6/22 永辉超市 298.50
  6/25 京东 - 书籍 156.00
  6/27 美团外卖 68.00
  6/28 支付宝 - 燃气费 86.00
  6/30 物美超市 198.00
```

**Execution Steps:**
1. All 19 items classified by category
2. Generate category breakdown with percentages
3. Detect spending patterns and provide suggestions

**Expected Output:**
```
=== 家庭支出报告（6月）===

| 日期   | 类别   | 金额   | 备注              |
|--------|--------|--------|-------------------|
| 6/1    | 购物   | 385.20 | 永辉超市          |
| 6/2    | 餐饮   | 128.50 | 美团买菜          |
| 6/3    | 其他   | 312.00 | 水电费            |
| 6/5    | 交通   | 42.00  | 滴滴打车          |
| 6/5    | 办公   | 89.00  | 京东打印机墨盒    |
| ...    | ...    | ...    | ...               |
| **合计** |        | **3188.30** |                   |

=== 类别汇总 ===
| 类别   | 笔数 | 金额     | 占比 |
|--------|------|----------|------|
| 购物   | 4    | 1,138.50 | 35.7% |
| 餐饮   | 5    | 799.80   | 25.1% |
| 交通   | 3    | 457.00   | 14.3% |
| 其他   | 3    | 497.00   | 15.6% |
| 办公   | 2    | 245.00   | 7.7%  |
| 通讯   | 1    | 99.00     | 3.1%  |

=== 财务建议 ===
📌 购物类支出占比最高（35.7%），可考虑减少非必需购物
📌 外卖/餐饮频次较高（6次），可增加家中做饭频率
📌 建议设定每月购物预算上限为800元
📌 无异常重复消费记录 ✅
```

---

## First-Success Path (30 Seconds)

```bash
# ──────────────────────────────────────────────────
#  30-SECOND FIRST SUCCESS
# ──────────────────────────────────────────────────

# Step 1 (5s): Run with a few expense lines
receipt-auditor --mode report --items "6/1 北京-上海高铁 553元"

# Step 2 (10s): Read the categorized output
# Step 3 (10s): Add more items or switch modes
receipt-auditor --mode audit --items $'6/1 超市 128.50\n6/1 超市 128.50'

# Step 4 (5s): Copy the formatted report to your reimbursement system!
```

### Quick-start for AI Assistants

```
Process the following expenses and generate a categorized report:
{mode: report, items: "6/1 北京-上海高铁 553元\n6/1 酒店 380元x2晚"}
Include: date, category, amount, description, category summary, total, and anomaly warnings.
```

### Verification Checklist

After running the skill, confirm:
- [ ] Mode matches the intended use case
- [ ] All line items parsed correctly (date, merchant, amount)
- [ ] Categories assigned correctly (verify 2-3 items manually)
- [ ] Total calculation is accurate
- [ ] Anomalies flagged (if any) are legitimate
- [ ] AA split totals verify against original amount
- [ ] Output is formatted as a clean Markdown table

---

## Error Handling

| Issue | Resolution |
|-------|-----------|
| Item missing date | Flag as "missing info" and still process |
| Amount format unclear | Flag as "amount unclear — verify manually" |
| Negative amount | Mark as refund/credit, separate from expenses |
| AA split totals don't match | Warn user: "Total mismatch by X元 — adjust manually" |
| Unrecognized category | Default to "Other" and log for user review |
| Empty input | Return: "No items to process — please provide bill text" |

---

## Key Differentiators

- **Semantic classification**: Understands Chinese merchant names and descriptions, not just keywords
- **Three specialized modes**: Report (reimbursement), AA Split (social), Audit (security) in one skill
- **Smart anomaly detection**: Catches duplicates, unusual amounts, and missing info automatically
- **Ready-to-submit output**: Markdown tables formatted for corporate reimbursement systems
- **AA logic**: Handles complex scenarios (shared items, personal items, exclusions like "brought own wine")
- **Privacy-first**: No data storage — process and forget

---

## License

MIT-0 — No attribution required.

---

## Changelog

- **v1.0.0** (2026-06-15): Initial release — three-mode expense auditor with intelligent classification, anomaly detection, and AA split calculation.
