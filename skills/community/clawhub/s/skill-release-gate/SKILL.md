---
title: "Skill Release Gate (Three Iron Rules)"
slug: skill-release-gate
display_name: 上架三铁律发布闸门
display_name_en: Skill Release Gate
compliance_review: 上架前由本闸门自审（国家/国际合规、AI友好、理念IP）
name: skill-release-gate
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
category: ai-agent
tags: [skill-release-gate, ai-agent, release-gate, desensitization]
author: SynomosAI
license: MIT
description: 所有 skill / MCP / 专家上架前必过的"上架三铁律"发布闸门——① 国家+国际合规 ② AI 特别友好 ③ 理念文化·强IP·好故事。含 A/B/C/D 分级加闸、GB45438 内容标识、五件套植入规范。内置可离线运行的安全扫描执行器（PII/密钥扫描、去敏复核）。
description_zh: "所有 skill/MCP/专家上架前必过的发布闸门：国家+国际合规、AI友好、理念强IP；A/B/C/D 分级加闸；内置离线 PII/密钥扫描与去敏复核，零外部依赖。"
description_en: "The mandatory release gate every skill / MCP / expert must pass before going public: (1) national+international compliance, (2) AI-friendly, (3) strong cultural/IP story. Includes A/B/C/D tiering, GB45438 labeling, and built-in offline PII/secret scanners plus desensitization re-check, zero external deps."
classification:
  skillhub: ["governance", "release-ops", "security"]
  iso_25010: ["Security", "Maintainability"]
read_when:
  - 任何 skill/MCP/专家/文档对外上架前要做发布前安检
  - 需要判定 A/B/C/D 分级、决定公链还是私有中心分流
  - 需要离线跑 PII/密钥扫描与去敏复核（0 命中才放行）
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/desens_check.py
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
- release-gate
- desensitization
- secret-scan
permissions:
  network: false
  filesystem: true      # read-write (扫描目标目录、生成报告)
  filesystem_scope: project-dir-only   # 仅限用户指定的目标目录，不越界
  subprocess: false
requirements:
  python_packages: []
  min_python: '3.8'
changelog: '1.0.1: Bilingual rewrite (EN-first) + read_when/classification added; 1.0.0 initial upload (USK v3 injected round2)'
---
> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

# Skill Release Gate (Three Iron Rules)

Every outward-facing artifact (skill / MCP / expert / document) must pass this gate before listing. Principle: **security first, release second; sensitive skills never go on public chains.**

## When to use
- Before listing any skill / MCP / expert / document (security first; sensitive skills never public).
- Triggers: release gate, three iron rules, secret scan, desensitization, pre-release check.

## How to use
```bash
python scripts/secret_scan.py --path <dir> --mode all   # PII+secret scan; 0 hits to pass
python scripts/desens_check.py --path <dir>             # desensit re-check; 0 hits to pass
```

## Workflow
1. Judge A/B/C/D tier;
2. Run secret_scan.py and desens_check.py;
3. Verify the five-piece set (signature / © / fingerprint / provenance / license);
4. Release only if the three iron rules hold; route C/D to the private center.

## 1. Three iron rules (policy layer — must pass)
1. **National + international compliance**: no political red lines, no sensitive geopolitics, target-market regulation (GB45438 content labeling, filing-trigger assessment).
2. **AI-friendly**: no discrimination, no misleading, explainable, human fallback; do not impersonate humans.
3. **Culture · strong IP · good story**: carries SynomosAI ethos with voice ambassador and five-piece set.

## 2. Tiered gating (A/B/C/D)
- **A (public chain)**: pure tech/methodology, no customer/pricing/registration detail → release after gate.
- **B (private center)**: industry know-how, brand structure, semi-sensitive → private registry only.
- **C (restricted)**: customer/channel/financial model → local SSOT only.
- **D (forbidden)**: secrets/PII/undesensitized internal data → never release.

## 3. Technical execution (built-in offline scanners)
```bash
python scripts/secret_scan.py --path <dir> --mode all   # exit 1 on leak -> block
python scripts/desens_check.py --path <dir>             # internal paths/hosts must be 0
```
- `secret_scan.py`: ID/phone/email/bank/address + API keys/tokens/PAT/private keys/bare Stripe live key/GitHub PAT.
- `desens_check.py`: internal absolute paths, intranet hosts (.internal/.local/.corp/.lan), workspace fragments.

## 4. Pre-release checklist
- [ ] Three iron rules met (A/B/C/D tier judged)
- [ ] secret_scan.py --mode all → 0 hits
- [ ] desens_check.py → 0 hits
- [ ] Five-piece set complete
- [ ] Sensitive (C/D) routed to private center, not mis-released

## Evidence & safety
- Evidence: TBD; Version: 1.0.1; Security: see bundled scanners; conclusions per scan output.

## 中文

# 上架三铁律发布闸门

所有对外发布物（skill / MCP / 专家 / 文档）上架前，必须依次过本闸门。原则：**先安检，后发布；敏感技能，绝不公链。**

## 何时用
- 所有 skill / MCP / 专家 / 文档对外上架前。
- 触发词：上架闸门、三铁律、secret scan、去敏、发布前安检。

## 用法
```bash
python scripts/secret_scan.py --path <待发布目录> --mode all   # PII+密钥扫描，0 命中才过
python scripts/desens_check.py --path <待发布目录>             # 去敏复核，0 命中才过
```

## 流程
1. 判 A/B/C/D 分级；2. 跑扫描；3. 核五件套；4. 满足三铁律后发布，C/D 分流私有中心。

## 一、三铁律
国家+国际合规 / AI 特别友好 / 理念文化·强IP·好故事。

## 二、分级加闸
A 公链公开 / B 私有中心 / C 受限本地 / D 禁发。

## 三、技术执行层
内置 `secret_scan.py`（PII+密钥）与 `desens_check.py`（内部路径/内网域名），零依赖离线跑，0 命中才放行。

## 四、发布前自检清单
三铁律逐条满足 / 两个扫描 0 命中 / 五件套齐全 / C/D 类已分流。

## 证据与安全声明
- 证据：TBD；版本：1.0.1；安全：见内置扫描器输出。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/skill-release-gate
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
