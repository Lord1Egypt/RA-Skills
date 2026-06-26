---
name: suanpan
description: 将用户自然语言交易描述转换为 suanpan CLI 命令。当用户提到记账、消费、支出、收入、转账、查账、统计等财务相关描述时触发。
---

# Suanpan 记账助手

Suanpan（算盘）是 Rust 编写的个人财务管理 CLI 工具，使用 SurrealDB 嵌入式数据库存储。

## 安装与依赖

### 依赖
- Rust 1.82+ (从源码编译时需要)

### 快速安装（推荐）
```bash
curl -sSL https://raw.githubusercontent.com/yinguobing/suanpan/main/install.sh | bash
```

### 从源码编译
```bash
git clone https://github.com/yinguobing/suanpan.git
cd suanpan
cargo build --release
sudo cp target/release/suanpan /usr/local/bin/
```

## 快速记账流程

1. **提取交易要素**（从用户自然语言中）
2. **构建命令**（使用 `suanpan add`）
3. **执行并反馈**

### 命令模板

```bash
# 支出（默认类型，可省略 -t expense）
suanpan add -a <金额> -f <来源账户> -c "<分类路径>" -d "<描述>"

# 收入
suanpan add -a <金额> -t income -f <来源> -c "收入/<子分类>" -d "<描述>"

# 转账
suanpan add -a <金额> -t transfer -f <来源账户> -o <去向账户> -c "转账"
```

### 交易类型判断

| 关键词 | 类型 | 示例 |
|--------|------|------|
| 花了、买了、支付 | `expense`（默认） | "午餐花了35" |
| 工资、收到、收入 | `income` | "收到工资8500" |
| 转、充值、提现 | `transfer` | "转1000到余额宝" |
| 借入、借款 | `debtchange` | "借入5000" |
| 借出、借钱给 | `creditchange` | "借给朋友2000" |

### 分类路径格式

使用 `"一级/二级"` 格式，如 `"餐饮/午餐"`、`"交通/地铁"`。

常用分类：
- 餐饮：早餐、午餐、晚餐、零食
- 交通：地铁、公交、打车、加油
- 购物：服装、数码、日用
- 居住：房租、水电、物业
- 收入：工资、奖金、投资

### 账户名称映射

直接使用用户提到的账户名（如"支付宝"、"招行卡"）。**注意**：账户需已存在，如不确定先执行 `suanpan account list` 查看。

## Gotchas（常见问题）

- **模糊搜索限制**：`--search` 在内存中过滤，大数据量时配合 `--limit 500` 或日期范围使用
- **分类路径格式**：必须使用 `"一级/二级"`，不是 `"一级-二级"` 或 `"一级:二级"`
- **账户存在性**：`add` 命令中的账户必须已存在，不存在时先用 `suanpan account add` 创建
- **ID 格式**：`remove` 和 `update` 使用短 ID（`list` 输出最后一列，前12位）
- **货币默认**：CNY，其他货币需显式指定 `-y USD`
- **转账必须有两个账户**：`-f`（来源）和 `-o`（去向）缺一不可
- **日期格式**：`--from` 和 `--to` 使用 `YYYY-MM-DD`，不是 `YYYY/MM/DD`

## 查询与统计

```bash
# 最近流水
suanpan list --limit 20

# 按日期范围统计
suanpan stats --from 2026-04-01 --to 2026-04-30

# 趋势分析
suanpan trend --period month
```

## 管理操作检查清单

### 添加账户
- [ ] 确认账户名称
- [ ] 选择账户类型：`e-wallet`、`bank-card`、`cash`、`investment`、`credit`、`debt`
- [ ] 执行 `suanpan account add "<名称>" -a <类型>`

### 修改/删除交易
- [ ] 执行 `suanpan list` 找到短 ID（最后一列）
- [ ] 更新：`suanpan update <短ID> -a <新金额>`
- [ ] 删除：`suanpan remove <短ID>`

### 批量导入
- [ ] 先使用 `--dry-run` 模拟导入
- [ ] 检查输出无错误后再正式导入

## 完整命令参考

根据场景选择参考文档：

| 场景 | 参考文档 |
|------|----------|
| 添加、查询、修改、删除交易记录 | [references/commands.md](references/commands.md) |
| 统计分析、趋势、报表 | [references/analytics.md](references/analytics.md) |
| 账户/分类/标签管理、数据导入 | [references/management.md](references/management.md) |

## 使用示例

### 支出记录
用户："今天午餐35块，用的支付宝"
```bash
suanpan add -a 35 -f 支付宝 -c "餐饮/午餐" -d "午餐"
```

### 收入记录
用户："昨天发工资8500到工资卡"
```bash
suanpan add -a 8500 -t income -f 公司 -c "收入/工资" -d "三月工资"
```

### 转账记录
用户："从招行卡转5000到余额宝"
```bash
suanpan add -a 5000 -t transfer -f 招行卡 -o 余额宝 -c "转账" -d "理财"
```

### 查询本周支出
用户："这周花了多少钱"
```bash
suanpan stats --from 2026-04-06 --to 2026-04-12
```
