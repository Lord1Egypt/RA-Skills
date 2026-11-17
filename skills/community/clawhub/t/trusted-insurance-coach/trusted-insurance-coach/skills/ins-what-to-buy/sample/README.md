# sample 目录说明

> **全部为合成案例，无真实个人、无真实收入数据、无真实保单。** 用于演示「买什么」的完整输入输出，可直接作为上架 demo 素材。

| 文件 | 场景 | 演示要点 |
|---|---|---|
| `demo_01_young_family.md` | 新手三口之家，"我该买什么、一年要花多少钱" | 信任三句 → 先问已有什么 → 先讲不用花的钱 → 配置顺序 → 预算区间 → 纸二 |
| `demo_02_already_full.md` | 老保单已交满，"还要不要再买" | 空间为负不加保 → 不劝退保 → 先做保单体检 → 复盘三问 |

对应生成的试算表输出：

- `output_01_budget_table.md`（正常区间：剩 7,000 元 ～ 2.2 万）
- `output_02_negative_room.md`（空间为负：先做保单体检，不加保）
- `output_03_dual_income.md`（两口子都挣钱：`--income 20 --income2 10` 合计成家庭收入）

生成命令（可复现）：

```bash
cd /workspace/insurance-advisor/skills/ins-what-to-buy
python3 scripts/budget_calc.py --income 30 --expense 12000 --existing 8000 \
  --output sample/output_01_budget_table.md
python3 scripts/budget_calc.py --income 15 --expense 8000 --existing 25000 \
  --output sample/output_02_negative_room.md
python3 scripts/budget_calc.py --income 20 --income2 10 --expense 10000 --existing 6000 \
  --output sample/output_03_dual_income.md
# 客户说不清精确数字时
python3 scripts/budget_calc.py --income 20-40 --mode rough
```

输出自检（应全部通过）：

```bash
cd /workspace/insurance-advisor
python3 scripts/compliance_scan.py --file skills/ins-what-to-buy/sample/demo_01_young_family.md
python3 scripts/compliance_scan.py --file skills/ins-what-to-buy/sample/demo_02_already_full.md
python3 scripts/compliance_scan.py --file skills/ins-what-to-buy/sample/output_01_budget_table.md
python3 scripts/compliance_scan.py --file skills/ins-what-to-buy/sample/output_02_negative_room.md
python3 scripts/compliance_scan.py --file skills/ins-what-to-buy/sample/output_03_dual_income.md
python3 scripts/compliance_scan.py --selftest
```
