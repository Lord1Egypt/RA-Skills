# skill-quality-gate · 技能质量门禁

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

**EN** — A skill isn't shippable just because it's written. 9-dimension gate: frontmatter fields · script compiles · icon · README · no secrets · bilingual · triggers · gate section · desensitized. Fail any → block publish. Runnable `quality_gate.py`. Theoretical root: LGD — gated (gate before publish).

**中文** — 9 维校验卡一道闸：frontmatter 八字段/脚本可编译/图标/README/无密钥/双语/触发词/门禁节/去敏。任一 fail 即拦截发布。附可运行脚本。理论根基：LGD 有门禁。

## Why it beats "publish and pray"

| Pain | This skill |
|---|---|
| Skill won't run | py_compile check |
| Leaks secrets | Secret-pattern scan |
| No docs / no zh-en | README + bilingual check |

## What's inside

- `SKILL.md` — 9 dimensions + 2-step flow + 铁律
- `scripts/quality_gate.py` — zero-dependency CLI: gate a skill dir

```bash
python scripts/quality_gate.py --dir ./my-skill
```

## Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| Market auto-review | Opaque | Transparent 9-dim, local |
| "Looks fine" | Subjective | Deterministic pass/fail |
| Manual checklist | Forgetful | Scripted, repeatable |

Theoretical root: **LGD Three Laws** — gated. Pairs with `release-gate`.

---

© 2026 SynomosAI SynomosAI · 代码 MIT · 理论文本保留所有权利

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


