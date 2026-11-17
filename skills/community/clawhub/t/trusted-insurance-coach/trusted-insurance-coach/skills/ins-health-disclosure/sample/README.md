# sample 目录说明

> **全部为合成案例，无真实个人、无真实病历、无真实保单。** 用于演示「健康告知陪审」的完整输入输出，可直接作为上架 demo 素材。

| 文件 | 场景 | 演示要点 |
|---|---|---|
| `demo_01_L1_newbie.md` | L1 新手，第一次买商业保险 | 分档 → 讲规则 → 出核对清单（full 模式）→ 收尾接续卡 |
| `demo_02_nodule.md` | 有甲状腺结节 + 五年前阑尾炎手术 | 逐题讲懂三段式 → 按体况找材料 → 核保路径建议 |
| `demo_03_card_lent.md` | 医保卡外借给妈妈买过降压药 | 外借专题 → 口述降级分支（`--mode oral`）→ 自证与告知口径 |

每个 demo 都包含：用户画像（合成）→ 用户输入 → 执行的命令 → 陪审输出示例 → 生成的清单文件。

对应生成的清单输出：

- `output_01_L1_newbie.md`
- `output_02_nodule.md`
- `output_03_card_lent.md`

生成命令（可复现）：

```bash
python3 scripts/disclosure_checklist.py --insurance-type 百万医疗 --role 本人 --findings "甲状腺结节 3mm" --output sample/output_01_L1_newbie.md
python3 scripts/disclosure_checklist.py --insurance-type 百万医疗 --role 本人 --findings "甲状腺结节 3mm; 5年前阑尾炎手术" --output sample/output_02_nodule.md
python3 scripts/disclosure_checklist.py --insurance-type 重疾 --role 本人 --findings "医保卡外借给妈妈买过降压药" --mode oral --output sample/output_03_card_lent.md
```

输出自检（应全部通过）：

```bash
python3 scripts/compliance_scan.py --file sample/output_01_L1_newbie.md
python3 scripts/compliance_scan.py --file sample/output_02_nodule.md
python3 scripts/compliance_scan.py --file sample/output_03_card_lent.md
python3 scripts/compliance_scan.py --selftest
```
