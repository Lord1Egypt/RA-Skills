---
name: publish-quality-gate
title: "Publish Quality Gate"
slug: publish-quality-gate
display_name: 发布质量门禁
display_name_en: Publish Quality Gate
version: 1.0.2
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
agent_created: true
author: SynomosAI
copyright: SynomosAI
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
category: security
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
description: >-
  Pre- and post-publish quality gate for any skill, expert pack, document or tool: four-layer sensitive-info checks (company → machine → personal → confidential) before release and TRACE five-dimension review after.

  发布质量门禁：发布任何 Skill/专家包/文档/工具到外部前后做质量检查——发布前四层敏感信息检查（公司→本机→个人→机密），发布后按 TRACE 五维（Trust/Reliability/Adaptability/Convention/Effectiveness）AI 自测。
description_zh: "发布质量门禁：发布任何 Skill/专家包/文档/工具到外部前后做质量检查——发布前四层敏感信息检查（公司→本机→个人→机密），发布后按 TRACE 五维（Trust/Reliability/Adaptability/Convention/Effectiveness）AI 自测。"
description_en: "Pre- and post-publish quality gate for any skill, expert pack, document or tool: four-layer sensitive-info checks (company → machine → personal → confidential) before release and TRACE five-dimension review after."
classification:
  skillhub: ["security-compliance", "release-engineering", "quality"]
  clawhub: ["development", "data-analytics"]
  iso_25010: ["Security"]
read_when:
  - 用户说「准备发布/发布前检查/检查一下发布物/脱敏检查」时
  - 发布任何 Skill/专家包/文档/工具到外部（分享/上架市场）前后
  - 需要对发布物做四层敏感信息审查与 TRACE 五维 AI 自测
risk_tier: medium
risk_rationale: "调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [publish-quality-gate, 发布质量, 发布前检查, 敏感扫描, 脱敏, TRACE, security-compliance]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/check_release.py
  runtime: python3
  call_pattern: args
output_schema:
  stdout: structured quality report (pass/fail per layer)
  exit_code: rc=0 ok / rc=1 warning / rc=2 bad input
changelog: "1.0.2: Bilingual rewrite (EN-first) + read_when added; risk_rationale ref neutralized; 1.0.1 prior"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

# Publish Quality Gate

## When to use
1. When a skill, expert pack, document, or tool is about to be distributed externally (shared or listed on a marketplace).
2. When the conversation hits triggers like "ready to publish", "desensitization check", or "TRACE review".
3. When four-layer sensitive-info review and TRACE five-dimension pre/post-publish validation are needed.

## How to use
- Core script: `python scripts/check_release.py`.
- Args: `--release_type` (content type) and `--mode` (pre/post publish).
- Trigger via natural language ("start desensitization") or by providing the artifact path.

## Workflow
1. Capture intent and confirm triggers.
2. Run four-layer sensitive-info checks (company → machine → personal → confidential) and block violations.
3. If post-publish, run the TRACE five-dimension (Trust/Reliability/Adaptability/Convention/Effectiveness) self-test.
4. Summarize results into a quality report with pass/fail status.
5. Report the final verdict and log the full detection record.

## Evidence & safety
- Evidence: TBD; Version: 1.0.2; Security: no independent scan (TBD).

## 中文

# 发布质量门禁

## 何时用
1. 用户计划把 Skill、专家包、文档或工具分发到外部平台（分享、上架市场）时。
2. 对话中出现「准备发布」「脱敏检查」「TRACE 评测」等触发词时。
3. 需要对发布物做四层敏感信息审查与 TRACE 五维 AI 自测的前后验证。

## 用法
- 核心脚本：`python scripts/check_release.py`。
- 参数：`--release_type`（内容类型）、`--mode`（发布前后）。
- 通过自然语言指令触发，或提供发布物路径。

## 流程
捕获意图并确认触发 → 执行四层敏感信息检查（公司→本机→个人→机密）并拦截违规 → 发布后启动 TRACE 五维 AI 自测 → 汇总生成质量报告标记通过/失败 → 反馈结论并记录检测日志。

## 证据与安全声明
- 证据：TBD；版本：1.0.2；安全：未做独立安全扫描（TBD）。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/publish-quality-gate
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/publish-quality-gate/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
