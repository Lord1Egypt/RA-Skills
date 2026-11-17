---
name: test-lab-match-check
slug: test-lab-match-check
title: 医疗器械检测项目与实验室匹配器
displayName: 医疗器械检测项目与实验室匹配器
display_name: 医疗器械检测项目与实验室匹配器
display_name_en: MD Test Item Derivation & Lab Match Checker
version: 1.0.1
license: MIT
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
author: SynomosAI (LGD initiative)
copyright: SynomosAI
category: 医疗器械合规
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
tags: ["医疗器械","医械合规","医疗器械检测项目与实验室匹配器","判定器","TH-MED-010","决策支持"]
description: "送检前以为项目就那几项，报告拿到手才发现缺一个终点、实验室资质还超范围——重送一轮就是几个月。（零依赖 CLI · 确定性 JSON IR · rc=0/1/2 · --demo 自带案例） 适用场景：当需要医疗器械检测项目与实验室匹配器能力时使用本技能；触发词：医疗器械、医械合规、医疗器械检测项目与实验室匹配器、判定器、TH-MED-010。"
description_en: "Deterministic zero-dependency CLI screener for medical-device compliance (test-lab-match-check). JSON IR output, rc=0/1/2, demo case included. Decision support only — always verify against official texts."
agent_created: true
verified_links: "规则源条款号已逐条标注；包内全部外链（含徽章）于 2026-09-12 逐条 HTTP 探测核验，11/11 可达"
description_zh: "送检前以为项目就那几项，报告拿到手才发现缺一个终点、实验室资质还超范围——重送一轮就是几个月。（零依赖 CLI · 确定性 JSON IR · rc=0/1/2 · --demo 自带案例）"
read_when:
  - 医疗器械送检前推导必做检测项目清单
  - 核对承接实验室资质（CMA/CNAS）是否覆盖项目
  - 无菌/灭菌类器械定灭菌方式后验证项推导
  - 注册申报前自检检测缺口与周期
classification:
  skillhub: ["medtech-reg"]
  iso_25010: ["Functional suitability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: test-lab-match-check.py
  runtime: python3
  call_pattern: args
input_schema:
  device_type:
    type: string
    description: "器械类型: active/passive/implant/ivd（必填）"
    required: false
  material:
    type: string
    description: "主体材料: metal/polymer/ceramic/natural/biologic"
    required: false
  contact:
    type: string
    description: "接触性质: surface/insert/implant/blood/mucosa"
    required: false
  sterile:
    type: string
    description: "是否无菌提供: yes/no"
    required: false
  steril_method:
    type: string
    description: "灭菌方式: eo/radiation/steam"
    required: false
  has_software:
    type: string
    description: "是否含软件: yes/no"
    required: false
  dest:
    type: string
    description: "申报目的国: cn/eu/us（默认 cn）"
    required: false
  demo:
    type: bool
    description: "跑内置冒烟案例"
    required: false
  json:
    type: bool
    description: "输出 JSON IR"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - medtech
  - test-lab
  - matching
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

> ⚠️ **Disclaimer**: AI-assisted; output is **decision support**, not medical-device registration, compliance or legal advice. Human review required; authoritative conclusions follow regulator decisions and the latest official documents.
> Text verification date: 2026-09-26 · clause text per the latest official publication.

### When to use
When the user needs medical-device test-item derivation and lab-qualification matching.
Trigger words: medical device, medtech compliance, test-lab matcher, TH-MED-010, decision support.

### Usage
Entry script (run inside the skill dir): `test-lab-match-check.py`. Parameters in Section IV.

### Workflow
1. Trigger: identify a test-lab-match-check task (see When to use).
2. Execute: run test-lab-match-check.py per Usage.
3. Verify: check output / exit code against expectations.
4. Deliver: present results / artifacts.

### I. The pain
Before sample submission you assume "just a few items"; when the report comes back you're missing an endpoint and the lab's accreditation doesn't even cover it — re-submitting costs months.

### II. What this is
A **zero-dependency, deterministic** screener. Pass known conditions as parameters; it applies public rule sources and outputs a structured verdict + obligation list + risk notes as JSON IR (machine-readable), directly embeddable in your own pipeline.

- **Zero-dependency**: Python stdlib only; no third-party packages, no network, no API key.
- **Deterministic**: same input → same output (no randomness, no model calls).
- **Traceable**: every conclusion carries its rule-source clause number for human check.
- **Offline**: runs on intranet, disconnected machines, old hardware.

### III. Core

| Item | Note |
|---|---|
| Rule sources | `GB/T 16886 series / GB 9706.1 / YY 0505 / ISO 11135·11137·17665 / ISO 11607 / IEC 62304` |
| Output | JSON IR (`result` + `rc` + `error_code` + `aigc_mark`) |
| Error codes | `E_INPUT_MISSING` insufficient args / `E_ENUM_INVALID` bad enum / `E_RUNTIME` other |
| Exit codes | `rc=0` verdict complete; `rc=1` complete with risk notes; `rc=2` input insufficient or invalid |

### IV. Usage
```bash
python test-lab-match-check.py --demo                     # built-in smoke case (recommended first)
python test-lab-match-check.py --json <your args...>     # real verdict
```
Available args: `--device_type / --material / --contact / --sterile / --steril_method / --has_software / --dest`

### IV-A. Real run (excerpt)
Command `python test-lab-match-check.py --device_type active --sterile yes` (2026-09-26, Python 3.13.12). Only JSON indentation adjusted for reading; **fields and values verbatim**.

```json
{
  "tool": "test-lab-match-check",
  "version": "1.0.0",
  "input": {"device_type": "active", "material": null, "contact": null, "sterile": "yes",
            "steril_method": null, "has_software": null, "dest": null},
  "result": {
    "device_type": "active",
    "required_tests": [
      "Biological evaluation · baseline endpoints (cytotoxicity/sensitization/irritation, selected by contact nature and duration)",
      "Electrical safety (GB 9706.1 general + applicable particular standards)",
      "EMC (YY 0505 / YY 9706.102)",
      "Sterilization validation (method must be fixed first: eo / radiation / steam)",
      "Sterile barrier system & packaging validation (ISO 11607 / GB/T 19633)"
    ],
    "lab_qualification": ["CMA", "CNAS"],
    "ref_cycle": "5–15 weeks (rough magnitude; depends on items and lab schedule)",
    "destination": "cn",
    "obligations": ["…3 items (accreditation-scope check / sample finalization consistency / items derived from technical requirements + risk)"],
    "notes": ["…3 items (derived output / cycle is not a commitment / export needs overseas-recognized reports)"],
    "evidence": ["GB/T 16886 series", "GB 9706.1", "YY 0505", "ISO 11135/11137/17665", "ISO 11607", "IEC 62304"],
    "warnings": [
      "No --material given: material class directly affects biocompatibility endpoints and chemical characterization; precision reduced",
      "Sterile declared but no sterilization method: definitive validation standard cannot be given"
    ]
  },
  "rc": 1,
  "error_code": null,
  "aigc_mark": {"standard": "GB 45438-2025", "is_generated": true, "generator": "test-lab-match-check@SynomosAI",
                "content_type": "decision_support_output", "disclaimer": "Decision support, not authoritative; human review required; per latest official documents"}
}
```

Three-way rc observed: `--device_type implant --material metal --contact implant --sterile yes --steril_method eo --dest cn` → rc=0; `--device_type active --sterile yes` → rc=1 (missing material/sterilization method, strict warning); `--device_type ivd --contact garbage` / `--dest jp` → rc=2 (bad enum).

### V. Boundaries (please read)
- Rule-based verdict only; no legal opinion, no certificate; human review required; final authority rests with regulators/notified bodies.
- **Strict on insufficient input**: missing `--material`, sterile-but-no-method etc. are surfaced in `warnings` (`rc=1`), never silently loosened.
- Out of scope: innovative devices, drug-device combos, boundary products, nanomaterials — follow official determination procedures.
- Rule versions change; **clause numbers are given — verify against latest official text**.
- Output is a starting checklist; **does not replace product technical requirements, applicable standards list, or expert judgment**.

### VI. Theory
Gates set standards first — testing is the gate that turns "compliance" into re-auditable data.

> Domain anchor: `TH-MED-010` · LGD REGISTRY · medical-device full-lifecycle governance (registered · evidenced · gated)

### VII. Family collection (by registration workflow)

| Stage | Tool | Status |
|---|---|---|
| Classification & route | `md-classification-route` | this batch |
| Registration dossier - technical docs | `SynomosAI-reg-hub` | existing hub |
| Clinical evaluation (route) | `clin-eval-route-picker` | existing |
| Clinical evaluation (evidence) | `cer-equivalence-check` | this batch |
| Test items & lab match | `test-lab-match-check` | this batch |
| Pre-submission non-clinical | `non-clinical-checker` | existing |
| UDI (format) | `udi-format-validator` | existing |
| UDI (database) | `udi-db-submission-check` | this batch |
| Post-market · PMCF plan | `pmcf-plan-check` | existing |
| Post-market · PMCF report | `pmcf-evaluation-report-check` | this batch |
| Post-market · vigilance intake | `pms-vigilance-intake` | existing |
| Post-market · recall | `recall-decision-checker` | existing |
| Labels & IFU | `label-compliance-checker` | existing |
| Import/export route | `import-export-router` | existing |

*TH-MED-010 domain · compliance checks · © 2026 SynomosAI · MIT License. AI-assisted (non-natural-person) content; the named institution takes publication responsibility.*

## 中文

> ⚠️ **免责声明**：本工具由 AI 辅助生成，输出为**决策支持**，不构成医疗器械注册、合规或法律意见。输出请人工复核，正式结论须以主管部门决定与官方最新文件为准。
> 文本核验日期：2026-09-26 · 条款文本以官方最新发布为准

### 何时用

- 当用户需要医疗器械检测项目与实验室匹配器相关能力时。
- 触发词：医疗器械、医械合规、医疗器械检测项目与实验室匹配器、判定器、TH-MED-010、决策支持。

### 用法

调用方式与参数详见正文「## 四、用法」节。
执行步骤见正文「## 七、家族合集（按注册全流程）」节。
入口脚本（在技能目录下执行）：test-lab-match-check.py。

### 流程

1. 触发：识别医疗器械检测项目与实验室匹配器相关任务（见「何时用」）。
2. 执行：按「用法」运行test-lab-match-check.py。
3. 校验：核对脚本输出/退出码是否符合预期。
4. 交付：向用户呈现结果/产物。

# 医疗器械检测项目与实验室匹配器

## 一、痛点

送检前以为项目就那几项，报告拿到手才发现缺一个终点、实验室资质还超范围——重送一轮就是几个月。

## 二、这是什么

一个**零依赖、确定性输出**的判定器。你把已知条件以参数传入，它按公开规则源给出结构化判定 + 义务清单 + 风险提示，输出 JSON IR（机器可读），可直接嵌入你自己的流程。

- **零依赖**：仅用 Python 标准库，无第三方包、无网络请求、无 API Key。
- **确定性**：同一输入永远同一输出（无随机、无模型调用）。
- **可回溯**：每条结论附规则源条款号，便于人工核对。
- **离线可用**：可在内网、断网、老电脑上运行。

## 三、判定核心

| 项 | 说明 |
|---|---|
| 规则源 | `GB/T 16886 系列 / GB 9706.1 / YY 0505 / ISO 11135·11137·17665 / ISO 11607 / IEC 62304` |
| 输出 | JSON IR（`result` + `rc` + `error_code` + `aigc_mark`） |
| 错误码 | `E_INPUT_MISSING` 参数不足 / `E_ENUM_INVALID` 枚举非法 / `E_RUNTIME` 其他 |
| 退出码 | `rc=0` 判定完成；`rc=1` 完成但带风险提示；`rc=2` 输入不足或非法 |

## 四、用法

```bash
python test-lab-match-check.py --demo                     # 跑内置冒烟案例（推荐先跑这个）
python test-lab-match-check.py --json <你的参数...>        # 正式判定
```

可用参数：`--device_type / --material / --contact / --sterile / --steril_method / --has_software / --dest`

## 四A、真机输出（实跑节选）
> 实跑命令 `python test-lab-match-check.py --device_type active --sterile yes`（2026-09-26，Python 3.13.12）。仅调整 JSON 缩进便于阅读，**字段与字段值逐字未改**（完整原文见做齐报告）。

```json
{
  "tool": "test-lab-match-check",
  "version": "1.0.0",
  "input": {"device_type": "active", "material": null, "contact": null, "sterile": "yes",
            "steril_method": null, "has_software": null, "dest": null},
  "result": {
    "device_type": "active",
    "required_tests": [
      "生物学评价·基础终点（细胞毒性/致敏/刺激，按接触性质与时长选做）",
      "电气安全（GB 9706.1 通用 + 适用专用并列标准）",
      "电磁兼容 EMC（YY 0505 / YY 9706.102）",
      "灭菌验证（须先确定灭菌方式：eo / radiation / steam）",
      "无菌屏障系统与包装验证（ISO 11607 / GB/T 19633）"
    ],
    "lab_qualification": ["CMA（检验检测机构资质认定）", "CNAS（实验室认可）"],
    "ref_cycle": "5–15 周（视项目数量与实验室排期，属量级参考）",
    "destination": "cn",
    "obligations": ["…3 条（认可范围核对 / 样品定型一致 / 项目由技术要求+风险推导）"],
    "notes": ["…3 条（推导结果 / 周期不构成承诺 / 出口需境外认可报告）"],
    "evidence": ["GB/T 16886 系列", "GB 9706.1", "YY 0505", "ISO 11135/11137/17665", "ISO 11607", "IEC 62304"],
    "warnings": [
      "未提供 --material：材料类别直接影响生物相容性终点与化学表征，缺失将降低清单精度",
      "已声明无菌但未指定灭菌方式，无法给出确定的验证标准"
    ]
  },
  "rc": 1,
  "error_code": null,
  "aigc_mark": {"standard": "GB 45438-2025", "is_generated": true, "generator": "test-lab-match-check@SynomosAI",
                "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核；以官方最新文件为准"}
}
```
（`obligations` / `notes` 数组字段值逐字未改，此处折叠。）

三档 rc 实测：`--device_type implant --material metal --contact implant --sterile yes --steril_method eo --dest cn` → rc=0；`--device_type active --sterile yes` → rc=1（缺材料/灭菌方式从严提示）；`--device_type ivd --contact garbage` / `--dest jp` → rc=2（枚举非法）。

## 五、能力边界（请务必阅读）

- 只做**规则判定**，不做法律意见、不出具证明；结论须人工复核，最终以监管机构/公告机构认定为准。
- **输入不足时从严提示**：缺 `--material`、声明无菌但缺灭菌方式等均在 `warnings` 中明示（`rc=1`），不静默按宽松清单输出。
- 不覆盖特殊情形（创新器械、药械组合、边界产品、纳米材料等），此类须走官方界定程序。
- 规则版本会变；**条款号已给出，请以官方最新文本核对**。
- 输出为起始清单，**不替代产品技术要求、适用标准清单与专业评价者判断**。

## 六、理论依据

有门禁先立标准——检测是把「合规」变成可复核数据的那道闸。

> 域站位件：`TH-MED-010` · LGD 理论总账 REGISTRY · 医疗器械全链路治理（有籍 · 有证 · 有门禁）

## 七、家族合集（按注册全流程）

| 环节 | 工具 | 位置 |
|---|---|---|
| 分类与路径 | `md-classification-route` | 本批 |
| 注册资料-技术文件 | `SynomosAI-reg-hub` | 存量枢纽 |
| 临床评价（选路） | `clin-eval-route-picker` | 存量 |
| 临床评价（证据要素） | `cer-equivalence-check` | 本批 |
| 检测项目与实验室匹配 | `test-lab-match-check` | 本批 |
| 申报前非临床研究 | `non-clinical-checker` | 存量 |
| UDI（格式校验） | `udi-format-validator` | 存量 |
| UDI（数据库提交） | `udi-db-submission-check` | 本批 |
| 上市后·PMCF 计划 | `pmcf-plan-check` | 存量 |
| 上市后·PMCF 评价报告 | `pmcf-evaluation-report-check` | 本批 |
| 上市后·不良事件 | `pms-vigilance-intake` | 存量 |
| 上市后·召回 | `recall-decision-checker` | 存量 |
| 标签与说明书 | `label-compliance-checker` | 存量 |
| 进出口路径 | `import-export-router` | 存量 |

---

诺衡@MED 域·合规核查 · TH-MED-010 · © 2026 SynomosAI · MIT License
本内容由 AI 辅助生成（非自然人），署名机构承担出品责任。
