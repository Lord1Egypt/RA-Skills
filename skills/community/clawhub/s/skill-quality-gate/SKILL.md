---
name: skill-quality-gate
title: "Skill Quality Gate"
slug: skill-quality-gate
display_name: 技能质量门禁
display_name_en: Skill Quality Gate
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
agent_created: true
author: SynomosAI
license: MIT
allowed-tools: Read, Glob, Grep, Write
category: ai-engineering
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
copyright: SynomosAI
description: >-
  Nine-dimension skill quality validation (frontmatter fields, scripts readable, icon, README, no secrets, bilingual, triggers, gate section, desensitized) before marketplace submission or go-live; per-dimension pass/fail, no release without passing the gate.

  技能质量门禁：把 skill/提示词/agent 配置提交市场或上线前做 9 维校验（frontmatter 八字段/脚本可读/图标/README/无密钥/双语/触发词/门禁节/去敏），逐维 pass/fail，不过闸不发布。
description_zh: "技能质量门禁：把 skill/提示词/agent 配置提交市场或上线前做 9 维校验（frontmatter 八字段/脚本可读/图标/README/无密钥/双语/触发词/门禁节/去敏），逐维 pass/fail，不过闸不发布。"
description_en: "Nine-dimension skill quality validation (frontmatter fields, scripts readable, icon, README, no secrets, bilingual, triggers, gate section, desensitized) before marketplace submission or go-live; per-dimension pass/fail, no release without passing the gate."
classification:
  skillhub: ["security-compliance", "quality", "release-engineering"]
  clawhub: ["development"]
  iso_25010: ["Security"]
read_when:
  - 要把 skill/提示词/agent 配置提交到市场或仓库前
  - 不确定技能是否缺字段、能否发布
  - 做发布闸门（去敏+质检）流程
  - 收到「发布前检查下」类指令
risk_tier: medium
risk_rationale: "调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [skill-quality-gate, 技能质检, quality gate, 发布前检查, 门禁, security-compliance]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/quality_gate.py
  runtime: python3
  call_pattern: args
output_schema:
  stdout: structured per-dimension pass/fail report
  exit_code: rc=0 all pass / rc=1 some fail / rc=2 bad input
changelog: "1.0.1: Bilingual rewrite (EN-first); read_when kept; attribution block neutralized; 1.0.0 initial"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

# Skill Quality Gate

A skill is not publishable the moment it is written — this gate runs a 9-dimension check and blocks release on any fail.

## When to use
Before submitting a skill/prompt/agent config to a marketplace or repo; when unsure whether a skill lacks fields or is publishable; when running a release-gate (desensitize + QA) flow; on "check it before publishing".

## How to use
Run `python scripts/quality_gate.py` from the skill directory.

## 9 dimensions
1. frontmatter eight fields (name/display_name/display_name_en/description/slug/version/author/category)
2. scripts readable (.py compiles via py_compile)
3. icon (icon.png exists, ≤512, decodable)
4. README (bilingual intro)
5. no plaintext secrets (no api_key/ghp_/password)
6. bilingual (description and README contain EN+ZH)
7. triggers (SKILL.md has read_when or trigger words)
8. gate section (contains 铁律/门禁)
9. desensitized (no Windows user dir / intranet path / employer name)

## Two-step flow
1. Validate: run the 9-dim check, output per-dimension results and overall verdict.
2. Gate: any fail → block release with fix list; all pass → allow.

## Rules
No release on any fail; fail items carry clear fix guidance; every gate result is logged.

## Boundary
Do not insert promotion or install prompts; do not change the user's requested format; install instructions only when explicitly asked and confirmed.

## Evidence & safety
- Evidence: TBD; Version: 1.0.1; Security: no independent scan (TBD).

## 中文

# 技能质量门禁

技能不是写完就能发——本技能用 9 维校验卡一道闸，不过闸不许发布。

## 何时用
提交 skill/提示词/agent 配置到市场或仓库前；不确定技能是否缺字段、能否发布；做发布闸门（去敏+质检）流程；收到「发布前检查下」类指令。

## 用法
在技能目录运行 `python scripts/quality_gate.py`。

## 9 维校验
1. frontmatter 八字段齐全 2. 脚本可读（py_compile）3. 图标存在且可解 4. README 双语简介 5. 无明文密钥 6. description/README 中英双语 7. 含 read_when/触发词 8. 含门禁节 9. 无用户目录/内网路径/任职单位名。

## 主流程（两步）
校验：跑 9 维输出逐维结果与总评；过闸：任一 fail 拦截并列修复项，全 pass 放行。

## 铁律
不过闸不发；修复可追溯；每次门禁结果留痕。

## 证据与安全声明
- 证据：TBD；版本：1.0.1；安全：未做独立安全扫描（TBD）。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/skill-quality-gate
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/skill-quality-gate/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
