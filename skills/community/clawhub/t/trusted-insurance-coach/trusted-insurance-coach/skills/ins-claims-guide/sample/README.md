# sample 目录说明

> **全部为合成案例，无真实个人、无真实病历、无真实保单。** 用于演示「理赔怎么办」的完整输入输出。

| 文件 | 场景 | 演示要点 |
|---|---|---|
| `demo_01_hospitalized.md` | A 情形：刚住院，还没报案 | 分档 → 五步流程前两步 → 材料清单（full 模式）→ 三条纪律 |
| `demo_02_rejected.md` | C 情形：收到拒赔通知 | 共情 → 要书面通知 → 证据保全 → 条款自查 → 复核 → 12378/调解 |
| `output_01_hospitalized.md` | 脚本输出：住院材料清单（完整版） | `claim_checklist.py` full 模式 |
| `output_02_materials_missing.md` | 脚本输出：材料不齐（不完整版） | `claim_checklist.py --mode oral` 降级分支 |
| `demo_03_waiting_for_money.md` | B+ 情形：材料交了在等钱 | 等钱三句话 → 提交日/受理号抓手 → 12378 超期反映 |

生成命令（可复现）：

```bash
python3 scripts/claim_checklist.py --insurance-type 百万医疗 --event 住院 \
  --hospital "三甲医院" --output sample/output_01_hospitalized.md
python3 scripts/claim_checklist.py --insurance-type 重疾 --event 确诊重大疾病 \
  --mode oral --output sample/output_02_materials_missing.md
```

输出自检（应全部通过）：

```bash
python3 scripts/compliance_scan.py --selftest                              # 11/11
python3 scripts/compliance_scan.py --file sample/demo_01_hospitalized.md
python3 scripts/compliance_scan.py --file sample/demo_02_rejected.md
python3 scripts/compliance_scan.py --file sample/output_01_hospitalized.md
python3 scripts/compliance_scan.py --file sample/output_02_materials_missing.md
```
