# tool-call-guard · 工具调用安全闸门

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — Treat every agent tool call as an *authorized action*. Grade by side-effect: read = allow, write = confirm, delete / send / pay = block. Ships a zero-dependency `tool_guard.py` that classifies a call and emits allow/block + reason.

**中文** — 把 agent 每次工具调用当需授权操作：按副作用分级，读放行、写确认、删/外发/支付拦截。附零依赖 `tool_guard.py` 给出级别与决策。

## Why it beats "give the agent all the tools"

| Pain | This skill |
|---|---|
| Agent silently `rm -rf` | L4 delete → blocked by default |
| Draft email auto-sent | L3 send → needs human confirm |
| One key to rule them all | Per-tool risk level, least privilege |
| "Who ran that?" | Every call audited (有证) |

## What's inside

- `SKILL.md` — 5-level risk model + 3-step gate flow + 铁律
- `scripts/tool_guard.py` — zero-dependency CLI: classify a tool call (name+args), emit level + allow/block + reason

```bash
python scripts/tool_guard.py --tool delete_file --args '{"path":"/data"}'
python scripts/tool_guard.py --tool send_email --args '{"to":"x","body":"y"}' --json
```

## Benchmark vs alternatives

| Tool | Gap this fills |
|---|---|
| MCP auth scopes | Runtime decision per call, not just static scope |
| "Just don't give delete tool" | Grained L0–L4, not binary |
| Manual review after | Pre-execution gate, not post-mortem |

Theoretical root: **LGD Three Laws** (registered · evidenced · gated). Pairs with `prompt-injection-shield` and `agent-redteam-kit`.

---

© 2026 SynomosAI. All rights reserved.

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 SynomosAI. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）
