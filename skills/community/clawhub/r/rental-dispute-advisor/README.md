# 租房押金纠纷助手 / Rental Dispute Advisor

处理中国租房押金不退、房东扣押金、提前退租、中介费、维修责任、涨租和退租争议。这个 skill 会把口头描述整理成事实清单、证据包、金额估算、催告函、投诉路径和协商话术。

> This is informational guidance only, not legal advice. For important legal matters, verify local rules and consult a licensed lawyer.

## Best Triggers

- 房东不退押金怎么办？
- 退租后房东说我弄坏家具/墙面/空调，要扣押金，合理吗？
- 提前退租押金还能要回来吗？
- 帮我写一封押金催告函给房东。
- 我要投诉房东/中介，应该找 12315、住建委还是街道调解？
- Help me recover my rental deposit in China.

## What It Produces

- Initial risk view: tenant-favorable, mixed-risk, landlord-favorable, or evidence-insufficient.
- Missing facts list: city, contract dates, deposit amount, move-out date, deduction reason, evidence.
- Evidence package: contract, payment proof, chat records, move-in/move-out photos, repair records.
- Compensation estimate: deposit refund, disputed deduction, breach amount, potential damages.
- Demand letter: a copy-ready Chinese notice to landlord or agency.
- Escalation path: negotiation, mediation, 12315, housing authority, arbitration, litigation.

## Fast Modes

| Mode | Best For |
|---|---|
| `quick_deposit_check` | 押金不退/扣押金的快速判断 |
| `evidence_pack` | 投诉、调解或起诉前整理材料 |
| `demand_letter` | 生成可复制的催告函 |
| `complaint_package` | 准备 12315/住建委/街道调解材料 |
| `negotiation_script` | 先协商，但要有边界和依据 |

## CLI

```bash
scripts/rental-dispute.sh collect --input my-case.json
scripts/rental-dispute.sh analyze --input my-case.json
scripts/rental-dispute.sh calculate --input my-case.json
scripts/rental-dispute.sh letter --type demand --input my-case.json
scripts/rental-dispute.sh evidence --input my-case.json
scripts/rental-dispute.sh negotiate --style firm --input my-case.json
scripts/rental-dispute.sh escalate --input my-case.json
```

## Good First Input

```text
我在上海租房，押金 6000 元，2026-06-01 退租。房东说墙面有污渍和空调损坏，要扣 3500 元。
我有合同、转账记录、搬出照片、3 月份告诉房东空调有问题的聊天记录。帮我判断能要回多少，并写催告函。
```

## Version

`1.1.0` improves Chinese marketplace discovery, deposit-dispute entry points, fast modes, README examples, and registry metadata.
