# 交易管理命令参考

核心交易操作命令：添加、查询、修改、删除流水记录。

## 命令概览

| 命令 | 功能 |
|------|------|
| `suanpan add` | 添加交易记录 |
| `suanpan remove` | 移除交易记录 |
| `suanpan update` | 更新交易记录 |
| `suanpan list` | 查询流水 |

---

## suanpan add

添加交易记录。

```bash
suanpan add -a <金额> -f <来源账户> [选项]
```

**参数：**

| 参数 | 短选项 | 长选项 | 说明 | 必填 | 默认值 |
|------|--------|--------|------|------|--------|
| 金额 | -a | --amount | 交易金额 | 是 | - |
| 类型 | -t | --tx-type | `expense`/`income`/`transfer`/`debtchange`/`creditchange` | 否 | expense |
| 来源 | -f | --from | 来源账户 | 是 | - |
| 去向 | -o | --to | 去向账户（转账时必填） | 否 | - |
| 分类 | -c | --category | 分类路径（如"餐饮/午餐"） | 否 | 其他 |
| 描述 | -d | --description | 交易备注 | 否 | - |
| 货币 | -y | --currency | 货币代码 | 否 | CNY |
| 标签 | -g | --tag | 标签（可多次使用） | 否 | - |

**示例：**

```bash
# 支出
suanpan add -a 35 -f 支付宝 -t expense -c "餐饮/午餐" -d "工作午餐"

# 收入
suanpan add -a 8500 -t income -f 公司 -c "收入/工资" -d "三月工资"

# 转账
suanpan add -a 1000 -t transfer -f 招行卡 -o 支付宝 -c "转账"

# 带标签
suanpan add -a 299 -f 京东白条 -t expense -c "购物/数码" -d "耳机" -g "2026-Q1" -g "必需品"
```

---

## suanpan list

查询流水记录。

```bash
suanpan list [选项]
```

**参数：**

| 参数 | 短选项 | 说明 |
|------|--------|------|
| `--limit <数量>` | -l | 返回记录数上限 |
| `--from <日期>` | | 日期范围开始（YYYY-MM-DD） |
| `--to <日期>` | | 日期范围结束（YYYY-MM-DD） |
| `--category <分类>` | | 按分类筛选 |
| `--account <账户>` | | 按账户筛选 |
| `--tx-type <类型>` | | 按交易类型筛选 |
| `--search <关键词>` | -s | 模糊搜索描述 |
| `--min-amount <金额>` | | 金额范围下限 |
| `--max-amount <金额>` | | 金额范围上限 |
| `--output <文件>` | | 导出到 CSV 文件 |

**示例：**

```bash
# 最近20条
suanpan list --limit 20

# 日期范围
suanpan list --from 2026-01-01 --to 2026-01-31

# 分类筛选
suanpan list --category "餐饮"

# 账户筛选
suanpan list --account "支付宝"

# 模糊搜索
suanpan list --search "地铁"

# 组合筛选+导出
suanpan list --from 2026-01-01 --to 2026-01-31 --search "午餐" --output lunch.csv
```

**输出格式：**

```
+---------------------------+--------+--------+------+----------+----------+-----------+----------+--------------+
| 时间                      | 类型   | 金额   | 货币 | 账户     | 去向     | 分类      | 备注     | ID           |
+================================================================================================================+
| 2026-04-11T12:30:00+08:00 | 支出   | 35.00  | CNY  | 支付宝   | -        | 餐饮/午餐 | 工作午餐 | a1b2c3d4e5f6 |
+---------------------------+--------+--------+------+----------+----------+-----------+----------+--------------+
```

---

## suanpan remove

移除交易记录。

```bash
suanpan remove <短ID> [短ID2] [短ID3] ...
```

**注意：** ID 从 `suanpan list` 输出最后一列获取，使用短 ID（前12位）即可。

**示例：**

```bash
suanpan remove f4sp877fxbwc
suanpan remove f4sp877fxbwc abc123dexy78 xyz789gh1234
```

---

## suanpan update

更新交易记录。

```bash
suanpan update <短ID> [选项]
```

**参数：** 与 `add` 相同，但所有参数可选，只更新指定字段。

**示例：**

```bash
suanpan update f4sp877fxbwc -a 40 -d "午餐+饮料"
suanpan update f4sp877fxbwc -c "餐饮/晚餐"
```

---

## 其他参考文档

- **统计分析**（stats/trend/compare）：见 [analytics.md](analytics.md)
- **数据管理**（account/category/tag/import）：见 [management.md](management.md)
