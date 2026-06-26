# 数据管理命令参考

当用户需要管理账户、分类、标签，或导入外部数据时参考本文档。

## 命令概览

| 命令 | 功能 |
|------|------|
| `suanpan account` | 账户管理（列表/添加/重命名/移除） |
| `suanpan category` | 分类管理（树形查看/添加/重命名/移除） |
| `suanpan tag` | 标签管理（列表/添加/重命名/移除） |
| `suanpan import` | 导入随手记 CSV/XLSX 文件 |

---

## 账户管理

### suanpan account list

列出所有账户。

```bash
suanpan account list
```

### suanpan account add

添加账户。

```bash
suanpan account add <名称> -a <类型> [--parent <父账户ID>]
```

**账户类型：**

| 类型 | 说明 |
|------|------|
| `e-wallet` | 电子钱包（支付宝、微信支付等） |
| `bank-card` | 银行卡 |
| `cash` | 现金 |
| `investment` | 投资账户（余额宝、理财等） |
| `credit` | 信用账户（信用卡、花呗等） |
| `debt` | 债务账户 |
| `other` | 其他 |

**示例：**

```bash
suanpan account add "支付宝" -a e-wallet
suanpan account add "招行卡" -a bank-card
suanpan account add "招招理财" -a investment --parent acc_cmb
```

### suanpan account rename

重命名账户。

```bash
suanpan account rename <ID或名称> <新名称>
```

**示例：**

```bash
suanpan account rename acc_alipay "Alipay"
suanpan account rename "支付宝" "Alipay"
```

### suanpan account remove

移除账户（需确保无流水关联、无子账户）。

```bash
suanpan account remove <ID或名称>
```

---

## 分类管理

### suanpan category tree

查看分类树。

```bash
suanpan category tree
```

### suanpan category add

添加分类（路径格式，自动创建各级）。

```bash
suanpan category add <路径>
```

**示例：**

```bash
suanpan category add "餐饮/午餐/食堂"
suanpan category add "交通/地铁"
```

### suanpan category rename

重命名分类（自动级联更新子分类）。

```bash
suanpan category rename <路径或ID> <新名称>
```

**示例：**

```bash
suanpan category rename "餐饮" "吃饭"
suanpan category rename cat_food "吃饭"
```

### suanpan category remove

移除分类（需确保无流水关联）。

```bash
suanpan category remove <路径或ID>
```

---

## 标签管理

### suanpan tag list

列出所有标签。

```bash
suanpan tag list
```

### suanpan tag add

添加标签。

```bash
suanpan tag add <名称> [--color <颜色>]
```

**示例：**

```bash
suanpan tag add "2026-Q1" --color "#FF0000"
suanpan tag add "必需品"
```

### suanpan tag rename

重命名标签。

```bash
suanpan tag rename <ID或名称> <新名称>
```

### suanpan tag remove

移除标签（自动从所有流水移除关联）。

```bash
suanpan tag remove <ID或名称>
```

---

## 数据导入

### suanpan import

导入随手记 CSV/XLSX 文件。

```bash
suanpan import <文件路径> [选项]
```

**参数：**

| 参数 | 说明 |
|------|------|
| `--format <格式>` | 文件格式：`csv`/`xlsx`（自动检测） |
| `--skip-duplicate` | 跳过重复记录 |
| `--dry-run` | 模拟导入（不实际写入） |

**示例：**

```bash
suanpan import ~/Downloads/随手记导出.csv
suanpan import ~/Downloads/随手记导出.xlsx --skip-duplicate
suanpan import ~/Downloads/随手记导出.csv --dry-run
```

**导入前检查清单：**
- [ ] 先用 `--dry-run` 模拟导入
- [ ] 检查输出是否有错误
- [ ] 确认无误后移除 `--dry-run` 正式导入
