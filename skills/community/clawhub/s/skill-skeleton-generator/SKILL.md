---
name: skill-skeleton-generator
description: >-
  One-command generator for LGD-compliant AI skill skeletons (SKILL.md + AGENTS.md + dirs) with full frontmatter scaffolding.

  一键生成符合 LGD 三律/四角度合规的新技能骨架（SKILL.md + AGENTS.md），规范化 frontmatter 起步。
slug: skill-skeleton-generator
title: skill-skeleton-generator
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
license: MIT
category: AI工程
author: SynomosAI (LGD initiative)
platforms: [windows, macos, linux]
tags: [skill, skeleton, generator]
description_zh: "一键生成符合 LGD 三律/四角度合规的新技能骨架（SKILL.md + AGENTS.md），规范化 frontmatter 起步。"
description_en: "One-command generator for LGD-compliant AI skill skeletons (SKILL.md + AGENTS.md + dirs) with full frontmatter scaffolding."
read_when:
  - 从零一键生成 LGD 三律/四角度合规的新技能骨架
  - 规范化 frontmatter（name/description/license/version/category/tags/slug/risk_tier）起步新技能
risk_tier: medium
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/skeleton.py
  runtime: python3
  call_pattern: args
input_schema:
  args:
    type: string
    description: CLI arguments per skill usage
    required: false
output_schema:
  stdout: structured result (JSON IR)
  exit_code: rc=0 ok / rc=1 warning / rc=2 bad input
capabilities:
- scaffold
- skeleton
- codegen
permissions:
  network: false
  filesystem: true
  subprocess: false
  scope: project-dir-only   # 只处理调用者指定目录，不越界、不跟随符号链接
requirements:
  python_packages: []
  min_python: '3.8'
changelog: '1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)'
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### Capabilities
- Generates SKILL.md with full frontmatter (name/description/license/version).
- Creates a machine-readable AGENTS.md entry and target directories.
- Four-angle (REG / TRUST / SAFE / MACH) compliant by construction.

### When to use
- Generate a new LGD-compliant skill skeleton from scratch (SKILL.md + AGENTS.md).
- Start a new skill with standardized frontmatter.

### Usage
```bash
python scripts/skeleton.py --name my-skill --description "..." [--out dir]
```

### Flow
1. Run `skeleton.py --name <skill> --description <desc> [--cat AI工程] [--out <dir>]`.
2. The script emits a SKILL.md with full frontmatter from an in-built TEMPLATE plus a machine-readable AGENTS.md.
3. Human edits the placeholder content (core capability / verification / usage) before entering the next quality gate.

### Evidence & safety
- Evidence: TBD. Version: 1.0.1. Security: no independent scan (TBD).

## 中文

### 功能
- 生成含完整 frontmatter 的 SKILL.md。
- 创建 AGENTS.md 机器可读入口与目录。
- 天然满足四角度合规（有籍/有证/有门禁/可机器读）。

### 何时用
- 当需要从零一键生成符合 LGD 三律/四角度合规的新技能骨架（SKILL.md + AGENTS.md）时使用本技能。
- 当需要规范化 frontmatter（name/description/license/version/category/tags/slug/risk_tier）起步一个新技能时使用本技能。

### 用法
```bash
python scripts/skeleton.py --name my-skill --description "..." [--out dir]
```

### 流程
1. 运行 `python scripts/skeleton.py --name <技能名> --description <描述> [--cat AI工程] [--out <输出目录>]`。
2. 脚本按内建 TEMPLATE 生成含完整 frontmatter 的 SKILL.md，并生成机器可读 AGENTS.md。
3. 人工编辑生成件中的占位内容（核心能力/验证/用法）后再进入后续质量门。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「新建一个技能，目录结构怎么搭」 / "Starting a new skill, how should the folders be laid out"
- 「帮我生成SKILL.md的骨架」 / "Generate a SKILL.md skeleton for me"
- 「技能的前置元数据老是写错」 / "I keep getting the skill frontmatter wrong"
- 「从零起一个技能要建哪些文件」 / "Which files does a skill need from scratch"
- 「有没有现成的技能模板可以直接改」 / "Is there a skill template I can just edit"
- 「骨架能按我们的规范生成吗」 / "Can the skeleton follow our internal conventions"

Trigger when the user says any of the above, in Chinese or English.

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/skill-skeleton-generator
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/skill-skeleton-generator/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
