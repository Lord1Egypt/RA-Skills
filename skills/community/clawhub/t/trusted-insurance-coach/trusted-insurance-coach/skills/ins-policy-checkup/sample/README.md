# sample 目录说明

> **全部为合成案例，无真实个人、无真实保单、无真实保单号。** 用于演示「保单体检」的完整输入输出，可直接作为上架 demo 素材。

| 文件 | 场景 | 演示要点 |
|---|---|---|
| `demo_01_messy_policies.md` | 家里四五张保单堆在抽屉里，"够不够" | 一次只录一单 → 九列检视表 → 三类缺口 → 三条纪律检查 → 纸一交给家人 |
| `demo_02_surrender.md` | 保费压力大，想退掉三张 | **不劝退也不劝留** → 只教看能退多少钱的那张表 → 三个自查问题 → 不算"划不划算"的账 |
| `policies_demo.json` | 3 张保单的输入数据（合成） | 字段格式示例 |

生成的检视表输出：

- `output_01_family_table.md`（含缺口、纪律检查、可直接喂预算的"已有保费支出"）

生成命令（可复现）：

```bash
cd /workspace/insurance-advisor/skills/ins-policy-checkup
python3 scripts/policy_review.py --input sample/policies_demo.json --income 30 \
  --output sample/output_01_family_table.md
python3 scripts/policy_review.py --demo        # 看内置示例
```

输出自检（应全部通过）：

```bash
cd /workspace/insurance-advisor
python3 scripts/compliance_scan.py --file skills/ins-policy-checkup/sample/demo_01_messy_policies.md
python3 scripts/compliance_scan.py --file skills/ins-policy-checkup/sample/demo_02_surrender.md
python3 scripts/compliance_scan.py --file skills/ins-policy-checkup/sample/output_01_family_table.md
python3 scripts/compliance_scan.py --selftest
```
