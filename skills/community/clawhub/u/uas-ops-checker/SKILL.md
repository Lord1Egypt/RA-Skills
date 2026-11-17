---
name: uas-ops-checker
slug: uas-ops-checker
displayName: 无人机运营合规分类判定器
version: 1.0.1
category: it-ops-security
display_name: 无人机运营合规分类判定器
title: 无人机运营合规分类判定器
author: 诺卫(SynomosAI)
author_note: '"SynomosAI" / "SynomosAI" — 未申请实体注册、未申请商标注册（not a registered legal entity; no trademark registered）'
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
description: 无人机运营合规分类判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-UAS-001域。 适用场景：当需要无人机运营合规分类判定器能力时使用本技能；触发词：合规、判定器、TH-UAS-001、uas-ops-checker。
tags: [合规, 判定器, TH-UAS-001, uas-ops-checker]
description_zh: "无人机运营合规分类判定器——基于官方规则源的零依赖决策支持工具，JSON IR 输出，覆盖TH-UAS-001域。"
description_en: "Drone operation compliance classification determination tool: zero-dependency decision support with JSON IR output (domain TH-UAS-001)."
read_when:
  - 按最大起飞重量/空机重量判定无人机运营合规等级
  - 输入不完整时要从严推定（义务最重者）
  - 自查微型/轻型/小型/中型/大型分类义务清单
  - 需要条款依据（evidence）与人工核对清单
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: uas-ops-checker.py
  runtime: python3
  call_pattern: args
input_schema:
  mtow:
    type: string
    description: "最大起飞重量(kg)"
    required: false
  empty_weight:
    type: string
    description: "空机重量(kg)"
    required: false
  demo:
    type: bool
    description: "跑内置冒烟案例"
    required: false
  json:
    type: bool
    description: "输出 JSON IR（默认）"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - drones
  - uas
  - compliance
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

> ⚠️ AI-assisted tool, decision reference only — not professional/legal advice, not a compliance certificate. Human review required; official authorities decide.
> Text self-check: 2026-09-26 · clause text per latest official publication.

### I. Pain point
Regulation is written across scattered documents; self-checking is costly and error-prone. This tool turns hard rules into an enumerable classifier.

### II. Boundaries
- Rule determination only, no legal advice; conclusions need human review.
- Rule sources: 《无人驾驶航空器飞行管理暂行条例》(State Council Order 761, effective 2024-01-01) articles 6/12/16/31/32 + CCAR-92 (clause numbers pending human check; always per latest official text).
- **Strict presumption on insufficient input**: with one weight given, concludes the heaviest-obligation plausible grade and warns the possible range (rc=1) — never silently outputs a lenient grade.
- Out of scope: airspace attributes, operator qualifications, insurance, cross-border/commercial review.

### III. Usage
```bash
python uas-ops-checker.py --mtow 5                    # only MTOW → strict presumption, rc=1
python uas-ops-checker.py --mtow 5 --empty_weight 4 # complete → light, rc=0
python uas-ops-checker.py --demo                     # built-in smoke (3 cases)
```
Args: `mtow` (max takeoff weight kg) / `empty_weight` (empty weight kg); at least one.

### IV. Real output (demo case 2 excerpt)
```json
{
  "tool": "uas-ops-checker",
  "input": {"mtow": "5"},
  "result": {
    "grade": "小型 (small)",
    "grade_basis": "strict presumption (incomplete input)",
    "possible_grades": ["micro", "light", "small"],
    "obligations": ["pilot license (per model)", "real-name registration", "mandatory liability insurance", "flight outside suitable airspace needs application"],
    "evidence": ["Interim Reg. art.6", "Interim Reg. art.16", "CCAR-92"],
    "warnings": ["incomplete input; category uses both MTOW and empty weight", "uncertain grade range micro~small; presumed heavy end"]
  },
  "rc": 1
}
```
Three cases: `mtow=0.2` → micro; `mtow=5` → small (strict presumption); `mtow=120` → medium; all rc=1.

### V. Exit codes
| rc | Meaning | Trigger |
|---|---|---|
| 0 | done, no warnings | complete params, micro/light grade |
| 1 | done with warnings | incomplete input (strict presumption) or small/medium/large |
| 2 | input insufficient/invalid | no args, non-numeric, empty > mtow, non-positive |

### VI. FAQ
- Q: Is this a compliance certificate? A: No, decision support only.
- Q: Only one weight? A: strict presumption, rc=1.
- Q: Rules outdated? A: per latest official text; `clause_review_checklist` maps each clause to its use.
- Q: Is identification reporting / flight upload "evidence"? A: No — per LGD semantics, evidence = verifiable basis of governance state transitions, not behavior logs.

### Theory
Every autonomous thing must first be registered, evidenced, gated — drone classification is the birth registration of air governance.

## 中文

> ⚠️ 本工具由 AI 辅助生成，仅供**决策参考**，不构成专业/法律意见，也不构成任何合规证明。输出请人工复核，并以主管部门认定为准。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准。

### 何时用
- 当用户需要无人机运营合规分类判定器相关能力时。
- 触发词：合规、判定器、TH-UAS-001、uas-ops-checker。

### 一、痛点
监管规则白纸黑字但散落多份文件，企业/个人自查成本高、易因错判触雷。本工具把硬规则变成可枚举的判定器。

### 二、能力边界
- 仅做**规则判定**，不做法律意见；结论须人工复核。
- 规则源：`《无人驾驶航空器飞行管理暂行条例》(国务院令761号,2024-01-01施行) 第6/12/16/31/32条 + CCAR-92`（条款号待人工核对）。
- **输入不足时从严推定**：只给一个重量参数时，取「可能等级中义务最重者」作为结论，并在 `warnings` 中明示（`rc=1`）。
- **不覆盖**：空域属性、运营主体资质、保险安排、涉外与商业运营的额外审查项。

### 三、用法
```bash
python uas-ops-checker.py --mtow 5
python uas-ops-checker.py --mtow 5 --empty_weight 4
python uas-ops-checker.py --demo
```
参数：`mtow`（最大起飞重量 kg）/ `empty_weight`（空机重量 kg）；至少给一个。

### 流程
1. 触发：识别无人机运营合规分类判定器相关任务（见「何时用」）。
2. 执行：按「用法」运行uas-ops-checker.py。
3. 校验：核对脚本输出/退出码是否符合预期。
4. 交付：向用户呈现结果/产物。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。
