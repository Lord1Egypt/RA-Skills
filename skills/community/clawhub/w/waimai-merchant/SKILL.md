---
name: waimai-merchant
version: 1.1.1
description: 外卖商家管理 Skill - 支持商家注册、商品管理、价格修改和配送时间设置。Use when user mentions merchant registration, product management, price updates, delivery time settings for food delivery business.
openclaw:
  permissions:
    filesystem: true
    database: true
  requires:
    node: ">=18.0.0"
triggers:
  - "商家注册"
  - "商品上传"
  - "修改价格"
  - "配送时间"
  - "waimai merchant"
  - "外卖商家"
---

# Waimai Merchant - 外卖商家管理

外卖商家管理系统，支持商家注册、商品管理、价格修改和配送承诺时间设置。

## 核心功能

1. **商家注册** - 商家信息录入、认证管理
2. **商品上传** - 添加新商品（名称、描述、图片、价格等）
3. **价格修改** - 更新商品价格
4. **配送承诺时间** - 设置/修改每个商品的承诺到货时间

## Operational Upgrade Workflow

Use this skill as an operations console, not a real platform integration. Before changing local merchant or product state, classify the request and show the exact target record.

1. **Classify intent**
   - Merchant onboarding or review
   - Menu/product creation
   - Price change
   - Delivery promise change
   - Stock/sold-out action
   - Suspension, rejection, deletion, or other high-risk admin action
2. **Preflight check**
   - Merchant id/status and product id/status
   - Old value and proposed new value
   - Reason, effective time, and rollback plan
   - Whether the change affects active customer-facing listings
3. **Confirmation rule**
   - Require explicit confirmation in the current turn for delete, reject, suspend, bulk price updates, delivery-time shortening, and any operation that can hide products or change customer promises.
   - Show a before/after diff for price, stock, delivery time, and status changes.
4. **Completion report**
   - Return the command run, changed ids, previous values, new values, and rollback command when available.
   - State that data is local SQLite data and is not synchronized to Meituan, Ele.me, or any live delivery platform.

Preferred response shape:

```text
Intent: <merchant | product | price | delivery | stock | admin>
Preflight: <target id, current state, requested change>
Action: <completed | needs confirmation | blocked>
Result: <changed ids and values>
Rollback: <command or manual step>
```

## 🔒 安全说明

### 权限声明
- **文件系统访问**: 此技能需要读写本地数据库文件，用于存储商家和商品信息
- **数据库操作**: 使用 SQLite 数据库 (`better-sqlite3`) 进行数据持久化
- **网络访问**: 无外部网络请求，所有操作在本地完成

### 安全边界
- ✅ 数据本地存储，不发送到外部服务器
- ✅ 使用标准 SQLite 数据库，无自定义二进制
- ✅ 代码开源可审计
- ❌ 不访问敏感系统文件
- ❌ 不执行特权操作

### 隐私保护
- 所有数据存储在 `~/.waimai-merchant/` 目录下
- 不收集用户身份信息
- 不记录使用行为数据

## 安装依赖

```bash
cd ~/.openclaw/workspace/skills/waimai-merchant
npm install
npm run build
```

## CLI 命令入口

### 商家管理命令

```bash
# 注册新商家
node dist/index.js merchant register -n "美味餐厅" -p "13800138000" -a "北京市朝阳区xxx街道"

# 列出所有商家
node dist/index.js merchant list

# 按状态筛选商家
node dist/index.js merchant list --status approved

# 查看商家详情
node dist/index.js merchant show <id>

# 更新商家信息
node dist/index.js merchant update <id> -n "新名称" -p "新电话"

# 认证商家
node dist/index.js merchant approve <id>

# 拒绝商家
node dist/index.js merchant reject <id>

# 暂停商家
node dist/index.js merchant suspend <id>

# 删除商家
node dist/index.js merchant delete <id>

# 搜索商家
node dist/index.js merchant search <keyword>
```

### 商品管理命令

```bash
# 添加新商品
node dist/index.js product add -m <merchant_id> -n "红烧肉" -p 38.00 -c "热菜" -t 30 -s 100

# 列出商品
node dist/index.js product list

# 按商家筛选商品
node dist/index.js product list -m <merchant_id>

# 只显示上架商品
node dist/index.js product list -a

# 按分类筛选
node dist/index.js product list -c "热菜"

# 查看商品详情
node dist/index.js product show <id>

# 更新商品信息
node dist/index.js product update <id> -n "新名称" -d "新描述"

# 修改商品价格
node dist/index.js product price <id> <new_price>

# 修改配送时间
node dist/index.js product delivery <id> <minutes>

# 上架商品
node dist/index.js product activate <id>

# 下架商品
node dist/index.js product deactivate <id>

# 标记售罄
node dist/index.js product soldout <id>

# 删除商品
node dist/index.js product delete <id>

# 搜索商品
node dist/index.js product search <keyword>

# 列出所有分类
node dist/index.js product categories
```

### 其他命令

```bash
# 查看数据存储位置
node dist/index.js data

# 显示帮助
node dist/index.js --help
node dist/index.js merchant --help
node dist/index.js product --help
```

## 数据结构

### 商家 (Merchant)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| name | TEXT | 商家名称 |
| phone | TEXT | 联系电话（唯一） |
| email | TEXT | 电子邮箱 |
| address | TEXT | 商家地址 |
| business_license | TEXT | 营业执照号 |
| contact_person | TEXT | 联系人姓名 |
| status | TEXT | 状态：pending/approved/rejected/suspended |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 商品 (Product)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| merchant_id | INTEGER | 商家ID（外键） |
| name | TEXT | 商品名称 |
| description | TEXT | 商品描述 |
| price | REAL | 当前价格 |
| original_price | REAL | 原价 |
| image_url | TEXT | 商品图片URL |
| category | TEXT | 商品分类 |
| delivery_time | INTEGER | 配送承诺时间（分钟） |
| stock | INTEGER | 库存数量 |
| status | TEXT | 状态：active/inactive/sold_out |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

## 数据存储

数据存储在: `~/.waimai-merchant/`
- `merchant.db` - SQLite 数据库文件

## 使用流程

### 商家入驻流程

1. **注册商家**: 使用 `merchant register` 录入基本信息
2. **等待审核**: 商家状态为 `pending`
3. **审核通过**: 管理员使用 `merchant approve` 通过认证
4. **开始营业**: 商家可以添加商品

### 商品管理流程

1. **添加商品**: 使用 `product add` 创建商品
2. **设置价格**: 初始价格可在添加时设置，后续用 `product price` 修改
3. **设置配送时间**: 初始配送时间在添加时设置，后续用 `product delivery` 修改
4. **上架销售**: 使用 `product activate` 将商品上架
5. **日常管理**: 根据库存情况使用 `product soldout` 或 `product deactivate`

## 技术栈

- **语言**: TypeScript / Node.js
- **数据库**: SQLite (better-sqlite3)
- **CLI 框架**: Commander.js
- **样式**: Chalk

## 扩展计划

以下功能为后续迭代方向：

- [ ] Web 管理界面
- [ ] 订单管理功能
- [ ] 数据统计报表
- [ ] API 接口开发
- [ ] 与 waimai-ai.ai 网站集成

---

## 🚀 First-Success Path

**30秒快速上手：三步管理外卖商家**

1. **注册商家** — 运行 `node dist/index.js merchant register -n "店名" -p "电话" -a "地址"`
2. **添加商品** — 运行 `node dist/index.js product add -m <商家ID> -n "菜品名" -p 价格 -c "分类" -t 配送时间(分钟)`
3. **上架营业** — 运行 `node dist/index.js product activate <商品ID>`，让商品对顾客可见

> 体验完整流程：注册 → 审核通过 → 添加商品 → 上架 → 查看商家信息

---

## 📝 Sample Prompts

### 示例 1：商家注册
**用户输入：**
```
帮我注册一个新外卖商家，店名叫"深夜食堂"，电话13800138000，地址在北京市朝阳区望京SOHO
```

**期望输出：**
```
✅ 商家注册成功！

商家信息：
━━━━━━━━━━━━━━━━━━
ID: 1
店名: 深夜食堂
电话: 13800138000
地址: 北京市朝阳区望京SOHO
状态: ⏳ pending（待审核）
━━━━━━━━━━━━━━━━━━

下一步：联系管理员审核通过后，你就可以添加商品了。

命令建议：
• 查看商家详情：`merchant show 1`
• 管理员审核：`merchant approve 1`
```

### 示例 2：添加商品
**用户输入：**
```
给深夜食堂（商家ID=1）加一道菜：红烧牛腩饭，38元，热菜类，配送承诺30分钟，库存100份
```

**期望输出：**
```
✅ 商品添加成功！

商品信息：
━━━━━━━━━━━━━━━━━━
ID: 1
名称: 红烧牛腩饭
价格: ¥38.00
分类: 热菜
配送时间: 30分钟
库存: 100份
状态: ❌ inactive（未上架）
━━━━━━━━━━━━━━━━━━

下一步：上架商品使其对顾客可见：
`product activate 1`
```

### 示例 3：修改价格
**用户输入：**
```
深夜食堂的红烧牛腩饭（商品ID=1）价格涨到42元
```

**期望输出：**
```
✅ 价格已更新！

商品: 红烧牛腩饭
原价: ¥38.00
现价: ¥42.00（+¥4.00）
更新时间: 2026-06-16 23:01

📊 你可以用 `product list -m 1` 查看该商家的全部商品和价格
```

### 示例 4：商家审核
**用户输入：**
```
审核通过深夜食堂（商家ID=1）的入驻申请
```

**期望输出：**
```
✅ 商家已审核通过！

商家: 深夜食堂
状态: pending → ✅ approved

商家现在可以：
• 添加商品（`product add`）
• 上架商品（`product activate`）
• 管理配送时间（`product delivery`）

📋 查看所有待审核商家：`merchant list --status pending`
```

### 示例 5：配送时间调整
**用户输入：**
```
把红烧牛腩饭（商品ID=1）的配送承诺时间改成25分钟
```

**期望输出：**
```
✅ 配送时间已更新！

商品: 红烧牛腩饭
原配送时间: 30分钟
新配送时间: 25分钟（-5分钟）

💡 缩短配送时间可提升顾客下单转化率，建议结合实际出餐能力设置，避免超时。
如需批量调整某商品的所有规格，可用 `product update 1 -d "配送时间下调至25分钟"`
```

---

## 📋 Real Task Examples

| 场景 | 用户输入示例 | 技能输出要点 |
|------|-------------|-------------|
| **新商家入驻** | "我想开个外卖店，需要怎么注册？" | 商家注册命令 + 填写信息模板 + 审核流程说明 + 审核后操作指引 |
| **菜品上架** | "新店刚开张，帮我加上8道菜" | 批量添加商品 → 设置分类/价格/配送时间 → 上架 → 确认库存 |
| **价格调整** | "最近原材料涨价，红烧肉从48涨到55" | 更新价格 → 确认历史价格可追溯 → 提示影响客单价 |
| **配送优化** | "厨房效率提高了，想把所有热菜的配送时间缩短5分钟" | 逐一或批量修改配送时间 → 确保不低于安全阈值 → 确认变更 |
| **商家管理** | "看看我们店里哪些菜下架了" | 按状态筛选商品 → 下架/售罄标注 → 查看原因 → 建议上架策略 |
