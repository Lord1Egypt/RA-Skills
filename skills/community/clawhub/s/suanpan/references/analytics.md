# 统计分析命令参考

当用户需要统计收支、查看趋势、生成报表时参考本文档。

## 命令概览

| 命令 | 功能 |
|------|------|
| `suanpan stats` | 统计分析 |
| `suanpan trend` | 趋势分析 |
| `suanpan compare` | 对比分析（环比/同比） |

---

## suanpan stats

统计分析。

```bash
suanpan stats [选项]
```

**参数：**

| 参数 | 说明 |
|------|------|
| `--month <YYYY-MM>` | 指定月份统计 |
| `--from <日期>` | 日期范围开始（YYYY-MM-DD） |
| `--to <日期>` | 日期范围结束（YYYY-MM-DD） |
| `--by-category` | 按分类统计（层级汇总） |
| `--by-account` | 按账户统计 |
| `--account <账户>` | 指定账户统计 |

**示例：**

```bash
# 按月统计
suanpan stats --month 2025-04

# 按分类统计
suanpan stats --by-category

# 按账户统计
suanpan stats --by-account

# 自定义日期范围
suanpan stats --from 2025-01-01 --to 2025-03-31

# 组合使用
suanpan stats --from 2025-01-01 --to 2025-03-31 --by-category

# 指定账户
suanpan stats --account 支付宝
suanpan stats --account 支付宝 --from 2025-01-01 --to 2025-01-31
```

---

## suanpan trend

趋势分析。

```bash
suanpan trend [选项]
```

**参数：**

| 参数 | 说明 |
|------|------|
| `--period <周期>` | 周期类型：`day`/`week`/`month`/`quarter`/`year` |
| `--from <日期>` | 日期范围开始 |
| `--to <日期>` | 日期范围结束 |
| `--by-category` | 按分类展示 |

**示例：**

```bash
# 按月趋势（默认最近6个月）
suanpan trend --period month

# 季度趋势
suanpan trend --period quarter --from 2025-01-01 --to 2025-12-31

# 周趋势按分类
suanpan trend --period week --from 2026-01-01 --to 2026-01-31 --by-category
```

---

## suanpan compare

对比分析（环比/同比）。

```bash
suanpan compare [选项]
```

**参数：**

| 参数 | 说明 |
|------|------|
| `--month <YYYY-MM>` | 指定月份 |
| `--compare-type <类型>` | 对比类型：`mom`（环比）/ `yoy`（同比）/ `all`（默认） |

**示例：**

```bash
# 完整对比（环比+同比）
suanpan compare --month 2026-01

# 仅环比（与上月对比）
suanpan compare --month 2026-01 --compare-type mom

# 仅同比（与去年同月对比）
suanpan compare --month 2026-01 --compare-type yoy
```

---


