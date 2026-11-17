# sample 目录说明

> **全部为合成案例，无真实个人、无真实合同、无真实核保结论。** 用于演示「怎么买」的完整输入输出，可直接作为上架 demo 素材。

| 文件 | 场景 | 演示要点 |
|---|---|---|
| `demo_01_clause.md` | 一份几十页看不懂的条款 | 不替他通读 → 定位险种 → 条款四看 → 先读责任免除 → "能不能买两份"的唯一依据 → 纸一 |
| `demo_02_exclusion.md` | 核保结论是「除外」，是不是被坑了 | 共情优先 → 五种结论速读 → 除外不是坏事 → 不劝退保 → 转健康告知陪审 |

对应生成的核对清单输出：

- `output_01_clause_list.md`（百万医疗：四看 + 续保专看 + 通用四项）

生成命令（可复现）：

```bash
cd /workspace/insurance-advisor/skills/ins-how-to-buy
python3 scripts/clause_check.py --insurance-type 百万医疗 \
  --output sample/output_01_clause_list.md
python3 scripts/clause_check.py --insurance-type 重疾
python3 scripts/clause_check.py --insurance-type 意外
python3 scripts/clause_check.py --insurance-type 定期寿险
```

输出自检（应全部通过）：

```bash
cd /workspace/insurance-advisor
python3 scripts/compliance_scan.py --file skills/ins-how-to-buy/sample/demo_01_clause.md
python3 scripts/compliance_scan.py --file skills/ins-how-to-buy/sample/demo_02_exclusion.md
python3 scripts/compliance_scan.py --file skills/ins-how-to-buy/sample/output_01_clause_list.md
python3 scripts/compliance_scan.py --selftest
```
