---
name: yaohx-expense-tracker
description: "个人记账助手。当用户发送消费信息（文本或支付截图）时自动识别并记录到本地消费数据库；支持按月归档、分类统计、查看消费记录、生成月度消费报告。触发词：记账、账单、消费记录、花了多少钱、月度总结、消费报告、看看本月消费等。This skill should be used when the user mentions recording an expense, checking spending, or requesting a consumption report."
agent_created: true
---

# 记账助手 (Expense Tracker)

## 概述

一个纯本地处理的个人记账技能。支持文本输入和支付截图两种方式记录消费，按月归档到本地 JSON 文件，支持消费分类管理、记录查询、月度报告生成。所有数据存储和处理均在本地完成，不依赖任何云端 API。

## 数据存储位置

所有数据文件存放在工作区根目录下（即当前工作目录）：

| 文件/目录 | 说明 |
|---|---|
| `categories.json` | 消费分类定义文件 |
| `expenses/` | 消费记录目录 |
| `expenses/expenses-YYYYMM.json` | 按月份的消费记录文件 |

数据格式详见 `references/data_schema.md`。

## 触发场景

1. **文本记账**：用户发送消费描述，如 "午餐花了25元"、"打车15块"
2. **图片记账**：用户发送微信支付/支付宝截图，直接识图后记录
3. **手动记录**：用户说"记账"并提供详细信息
4. **查看记录**：用户说"看看本月消费"、"本月花了多少"
5. **月度报告**：用户说"生成本月消费报告"、"月度总结"
6. **删除记录**：用户说"删除刚才那条记录"、"删掉某笔消费"

## 工作流程

### 初始化（首次使用时执行）

当用户首次使用记账功能时，先执行初始化：

```bash
python scripts/init_db.py
```

此脚本在工作区根目录创建：
- `categories.json`（含默认分类）
- `expenses/` 目录
- 当前月份的 `expenses/expenses-YYYYMM.json` 空文件

### 流程 A：处理文本账单

1. 从用户消息中提取关键信息：日期、时间、金额、商家、消费类别、支付方式、备注
2. 如果用户未提供日期/时间，默认使用当前日期和时间
3. 根据商家名称和备注，自动匹配消费分类（匹配规则见下方）
4. 调用脚本写入记录
5. 回复用户确认记录成功，展示本次消费摘要和本月累计

**关键：调用脚本时使用独立参数，绝不传递 JSON 字符串**

正确调用方式：

```bash
python scripts/record_expense.py --amount 25 --merchant "兰州拉面" --category "餐饮" --date 2026-07-09 --time 1230 --payment "微信" --note "午餐"
```

参数说明：
- `--amount`：金额（数字，必填）
- `--merchant`：商家名称（必填）
- `--category`：消费分类（可选，不传则自动匹配）
- `--date`：日期，格式 YYYY-MM-DD（可选，默认今天）
- `--time`：时间，格式 HHMM（可选，默认当前时间）
- `--payment`：支付方式（可选，如 微信/支付宝/现金/银行卡）
- `--note`：备注（可选）

### 流程 B：处理图片账单（支付截图）

**根据模型能力选择路径：**

#### 路径 B1：多模态模型（能直接识图）

如果你是多模态模型，可以直接观察图片：

1. 用户发送支付截图后，直接观察图片，提取以下信息：
   - 金额（必填）
   - 商家/收款方名称
   - 支付方式（微信/支付宝等）
   - 交易时间（如图片中可见）
   - 备注/商品说明
2. 将提取结果展示给用户确认（如有不确定的信息请用户补充）
3. 用户确认后，使用独立参数调用 `record_expense.py` 写入记录
4. 回复确认

#### 路径 B2：非多模态模型（无法识图，使用本地 OCR）

如果你无法直接观察图片（非多模态模型），使用本地 OCR 脚本提取文字：

1. 获取用户发送的截图文件路径
2. 调用 OCR 脚本提取文字和结构化信息：

```bash
python scripts/ocr_image.py --image "截图文件路径"
```

脚本使用 rapidocr-onnxruntime 进行本地 OCR：

3. OCR 脚本输出 JSON 格式结果：

```json
{
  "success": true,
  "raw_text": "微信支付 ¥25.00 向兰州拉面付款...",
  "structured": {
    "amount": 25.00,
    "merchant": "兰州拉面",
    "date": "2026-07-09",
    "time": "1230",
    "payment": "微信",
    "note": null
  },
  "method": "rapidocr"
}
```

4. 读取 `structured` 中的字段，如果关键信息（金额、商家）已提取到，展示给用户确认后调用 `record_expense.py` 写入记录
5. 如果 `structured` 中部分字段为 null，根据 `raw_text` 上下文自行推断补充，或请用户手动补充缺失信息
6. 如果 OCR 脚本返回 `"success": false`，说明 OCR 不可用，此时**必须**请用户手动输入消费信息（金额、商家等），不要直接报错终止

OCR 不可用时输出示例：
```json
{
  "success": false,
  "error": "rapidocr-onnxruntime not installed",
  "install_hint": "pip install rapidocr-onnxruntime",
  "fallback_instruction": "OCR is not available. Please ask the user to manually input the expense details."
}
```

**OCR 依赖安装（非多模态模型必须安装）：**

如需使用图片记账功能，运行：
```bash
python -m pip install rapidocr-onnxruntime
```

如果未安装 rapidocr，OCR 脚本会返回 `fallback_instruction`，此时必须请用户手动输入消费信息。
多模态模型不需要安装 OCR——直接识图即可。

### 流程 C：查看消费记录

调用脚本查询：

```bash
# 查看指定月份
python scripts/list_expenses.py --month 202607

# 查看指定月份某分类
python scripts/list_expenses.py --month 202607 --category "餐饮"

# 不传 --month 则默认当前月
python scripts/list_expenses.py
```

### 流程 D：生成月度消费报告

```bash
# 指定月份
python scripts/generate_report.py --month 202607

# 不传则默认当前月
python scripts/generate_report.py
```

报告内容包含：
- 本月总支出金额
- 各分类支出金额及占比
- 日均消费金额
- 单笔最高消费
- 支付方式分布
- 与上月对比（如果上月数据存在）

将报告摘要回复给用户，可配合 show_widget 展示饼图或柱状图。

### 流程 E：删除消费记录

```bash
python scripts/delete_expense.py --id 2026-07-09-001
```

删除后回复用户确认。

## 消费分类自动匹配规则

当用户未明确指定分类时，根据商家名称和备注自动匹配：

- 含"餐、饭、面、粉、菜、外卖、咖啡、奶茶、饮料、零食、烧烤、火锅、早点、早餐、午餐、晚餐、夜宵"等 → `餐饮`
- 含"打车、滴滴、公交、地铁、加油、停车、充电、单车、出租、高铁、火车、机票、飞机"等 → `交通`
- 含"超市、便利店、淘宝、京东、拼多多、天猫、苏宁、网购"等 → `购物`
- 含"房租、房贷、水电、燃气、物业、宽带"等 → `居住`
- 含"电影、KTV、游戏、旅游、景点、门票、健身"等 → `娱乐`
- 含"医院、药房、诊所、挂号、药"等 → `医疗`
- 含"话费、流量、充值"等 → `通讯`
- 含"衣服、鞋、裤、裙、外套、服装"等 → `服饰`
- 含"书、课程、培训、学费、教育"等 → `教育`
- 其他默认归入 `其他`

## 脚本调用注意事项

### 绝不传递 JSON 字符串

所有脚本均使用 `argparse` 接收独立参数。不要将数据组装成 JSON 字符串再传给脚本。这是为了避免 Windows 下 shell 引号转义问题。

错误示例（会导致 Windows 下引号冲突）：
```bash
python scripts/record_expense.py '{"amount": 25, "merchant": "兰州拉面"}'
```

正确示例（独立参数，无嵌套引号问题）：
```bash
python scripts/record_expense.py --amount 25 --merchant "兰州拉面"
```

### 使用 python 而非 python3

在 Windows 上，`python3` 命令通常不存在。始终使用 `python`。

### 中文参数

中文参数用双引号包裹即可，不需要额外转义：
```bash
python scripts/record_expense.py --amount 25 --merchant "兰州拉面" --category "餐饮"
```

### 脚本路径

脚本路径相对于 skill 目录。脚本内部会自动以当前工作目录作为数据存储根目录。如需指定其他数据目录，使用 `--data-dir` 参数：
```bash
python scripts/record_expense.py --amount 25 --merchant "兰州拉面" --data-dir "C:\Users\me\my-expenses"
```

## 脚本清单

| 脚本 | 功能 | 关键参数 |
|---|---|---|
| `scripts/ocr_image.py` | OCR 识别截图文字（非多模态模型用） | `--image`（必填） |
| `scripts/init_db.py` | 初始化数据文件 | `--data-dir`（可选） |
| `scripts/record_expense.py` | 记录一笔消费 | `--amount`, `--merchant`, `--category`, `--date`, `--time`, `--payment`, `--note` |
| `scripts/list_expenses.py` | 查询消费记录 | `--month`, `--category`（均可选） |
| `scripts/generate_report.py` | 生成月度报告 | `--month`（可选，默认当月） |
| `scripts/delete_expense.py` | 删除一条记录 | `--id` |

## 数据格式

数据格式详见 `references/data_schema.md`。

## 注意事项

- `expenses-YYYYMM.json` 中 `id` 格式为 `YYYY-MM-DD-NNN`，NNN 为当天序号（001 起），同一日期内递增
- 每次写入后自动更新 `last_updated` 时间戳
- 金额保留原始精度，汇总时四舍五入到两位小数
- 所有 Python 脚本使用 UTF-8 编码
- 脚本输出为 JSON 格式，方便模型解析
