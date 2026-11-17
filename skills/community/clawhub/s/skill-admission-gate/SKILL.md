---
title: "skill-admission-gate"
slug: skill-admission-gate
displayName: "skill-admission-gate"
category: "lgd-theory"
compliance_review: "待核验：上架三铁律 ①国家/国际合规 ②AI特别友好 ③理念文化传播+强IP；发布前由 skill-release-gate 审查"
name: skill-admission-gate
description: >-
  Scan a skill or plugin before installation and block destructive commands, remote execution, data exfiltration, prompt injection, obfuscated payloads and scope overreach.

  技能上架安全闸门——一个技能/插件在安装或上架前，先跑确定性安全审查：查破坏性命令、远程执行、数据外泄、提示注入、隐蔽行为、混淆载荷与作用域越界，产出「分级发现 + 闸门判定 + 包指纹证据」。当需要审查第三方 skill、安装来源不明的技能、给自研技能做发布前安检、做供应链安全评估、或需要出具"该包未被篡改且已评估风险"的证据时调用。核心三件事：①按规则集扫全部文件并分级（BLOCK/WARN）②支持"已接受风险"声明（.admission-allow.json，须署名留痕）③输出包指纹与文件哈希作为"有证"产物。触发词：技能安全、审查 skill、安装前检查、恶意技能、skill 安全扫描、上架闸门、供应链安全、这个技能安全吗、第三方技能、能不能装、木马、后门、提示注入。
version: 1.0.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, WebFetch
agent_created: true
author: XLGD · SynomosAI
description_zh: "技能上架安全闸门——一个技能/插件在安装或上架前，先跑确定性安全审查：查破坏性命令、远程执行、数据外泄、提示注入、隐蔽行为、混淆载荷与作用域越界，产出「分级发现 + 闸门判定 + 包指纹证据」。当需要审查第三方 skill、安装来源不明的技能、给自研技能做发布前安检、做供应链安全评估、或需要出具\"该包未被篡改且已评估风险\"的证据时调用。核心三件事：①按规则集扫全部文件并分级（BLOCK/WARN）②支持\"已接受风险\"声明（.admission-allow.json，须署名留痕）③输出包指纹与文件哈希作为\"有证\"产物。触发词：技能安全、审查 skill、安装前检查、恶意技能、skill 安全扫描、上架闸门、供应链安全、这个技能安全吗、第三方技能、能不能装、木马、后门、提示注入。"
description_en: "Scan a skill or plugin before installation and block destructive commands, remote execution, data exfiltration, prompt injection, obfuscated payloads and scope overreach. It grades every finding as block or warn, records accepted risks with a signature, and returns a package fingerprint plus file hashes as tamper evidence."
read_when:
  - 安装第三方/来源不明的技能前
  - 自研技能发布前要做安全前置审查
  - 批量做技能供应链安全评估
  - 需要「包未被篡改且已评估风险」的证据
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [skill-admission-gate, lgd-theory, 供应链安全, 上架闸门]
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/scan_skill.py
  runtime: python3
  call_pattern: args
input_schema:
  batch:
    type: bool
    description: "对根目录下每个子目录分别审查"
    required: false
  json:
    type: string
    description: "结果写入 JSON"
    required: false
  quiet:
    type: bool
    description: "quiet"
    required: false
  target:
    type: string
    description: "技能目录，或 --batch 时的技能根目录"
    required: true
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - skill
  - admission
  - gate
permissions:
  network: true
  filesystem: true
  subprocess: true
  scope: project-dir-only   # 只处理调用者指定目录；外发需人逐次确认，无预设接收端
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
Call this when you need to review a third-party skill, install a skill of unknown provenance, run pre-release security screening on an in-house skill, perform a supply-chain security assessment, or produce evidence that "this package is untampered and risk-assessed".

### Usage
Entry script (run inside the skill directory): `scan_skill.py`.

### Workflow
1. Trigger: identify a skill-admission-gate task (see When to use).
2. Execute: run scan_skill.py per Usage.
3. Verify: check script output / exit code against expectations.
4. Deliver: present results / artifacts to the user.

> **Executable implementation of the LGD Three Laws**: registered (package fingerprint) · evidenced (scan evidence on record) · gated (verdicts and accepted risks must be signed).
> Rule set `1.0.0` · stdlib only · offline-runnable · no API key.

### I. Why it is needed
The security problem of the skill ecosystem is **not "are there malicious packages" but "there is no admission gate"**:

- Skills can execute arbitrary code, access the filesystem and make network requests — their permission surface equals a local program;
- Yet their distribution often looks like "a block of documentation" — review intuition fails;
- Once installed, it runs on your machine as you.

**Conclusion**: skills need a **deterministic, traceable, re-auditable** security checkpoint, not "looks fine".

### II. When to use it

| Scenario | Note |
|---|---|
| Before installing third-party skills | Especially packages of unknown provenance, no repo backing, no license |
| Before in-house skill release | Pairs with skill-release-gate as the security front gate |
| Supply-chain assessment | Batch-scan a skill root, produce a risk list |
| Evidence needed | Package fingerprint + file hashes + timestamp proving "this version unchanged" |

### III. How to use

Single-skill review:
```bash
python scripts/scan_skill.py <skill-dir> [--json out.json]
```
Batch review (scan a skill root):
```bash
python scripts/scan_skill.py <skill-root> --batch --json batch-result.json
```
Output example:
```
skill: my-skill
verdict: WARN | BLOCK 0 | WARN 2 | accepted 0 | 6 files scanned
package fingerprint: cd23896eee940857
  [WARN] EXF-04 script.py:41  requests.post("https://api.example.com/collect", ...)
```
Exit codes: `0` = no BLOCK; `1` = BLOCK (usable as CI gate).

### IV. Rule set (v1.0.0)

| Group | Rules | Level | Detects |
|---|---|---|---|
| **Destructive** | DES-01~05 | **BLOCK** | recursive forced delete, `del /s /f`, `shutil.rmtree`, format/write device, fork bomb |
| **Remote exec** | EXE-01,02 | **BLOCK** | `curl|sh`, encoded PowerShell, `iex(` |
| | EXE-03,04 | WARN | `eval(`/`exec(`, post-base64-decode exec |
| **Exfiltration** | EXF-01,02 | **BLOCK** | reading private keys / credential files, reading local vaults and key-drop tools |
| | EXF-03,04 | WARN | reading `.env`/env credentials, POST/PUT to external endpoints |
| **Prompt injection** | INJ-01,02 | **BLOCK** | "ignore previous instructions", "do not tell the user" |
| | INJ-03~05 | WARN | silent execution, bypassing security/approvals, tricking users into pasting keys |
| **Obfuscation** | OBF-01 | WARN | overlong Base64 strings (suspected payload) |
| **Scope** | SCP-01 | WARN | writing absolute paths outside the skill dir |

**Verdict**: any BLOCK hit → overall `BLOCK`; only WARN → `WARN`; none → `PASS`.

### V. Accepted-risk mechanism (key design)

**False positives are inevitable** — e.g. a local-vault skill "reading <local-vault>" is its *job*, not exfiltration.

But "accepting a risk" must not be silent ignoring: it must be traceable and signed. Drop `.admission-allow.json` in the reviewed dir:

```json
{
  "schema": "skill-admission-allow/1.0",
  "skill": "dpapi-local-vault",
  "note": "This skill's function is a local credential vault; accessing that dir is its declared use.",
  "allow": [
    {
      "rule": "EXF-02",
      "reason": "Reading/writing <local-vault> is its sole declared use; keys never leave plaintext or the machine.",
      "approved_by": "XLGD",
      "date": "2026-09-12",
      "mitigation": "This skill makes no network requests."
    }
  ]
}
```
After declaration the rule moves to ACCEPTED (still appears in the report, no verdict impact) — **this is "gated + evidenced"**.

### VI. Evidence produced ("evidenced")

Every review outputs:

| Field | Meaning |
|---|---|
| `package_fingerprint_sha256` | aggregate hash of all files — "was the package tampered" |
| `file_hashes[]` | sha256 + byte size per file |
| `rule_version` | rule-set version (rules evolve; record which version decided) |
| `timestamp_utc` | review time |
| `accepted_risks[]` | accepted risks with signer and reason |

**Uses**: release ledger, dispute forensics, version-regression comparison (fingerprint changed → re-review required).

### VII. Boundaries & honesty

- **Pattern matching has limits**: this tool checks *known patterns*; it stops crude and common tricks but **cannot replace human code audit**; coverage of heavy obfuscation, logic backdoors and dependency-chain poisoning is weak.
- **No sandbox execution**: static review only; no dynamic behavior analysis.
- **Rules evolve**: verdicts depend on `rule_version`; align rule versions when comparing across versions.
- **No security guarantee**: `PASS` means "no hit against this rule set", **not "secure"**.

### VIII. Mapping to LGD

| LGD law | This skill's implementation |
|---|---|
| **Registered** | Package fingerprint + file hashes: uniquely identify "who / which version" |
| **Evidenced** | scan findings + rule version + timestamp, all persisted to JSON |
| **Gated** | BLOCK blocks (exit 1); accepting a risk requires signer + reason + mitigation |

*skill-admission-gate v1.0.1 · © XLGD · SynomosAI · 2026-09-12*

## 中文

### 何时用

- 当需要审查第三方 skill、安装来源不明的技能、给自研技能做发布前安检、做供应链安全评估、或需要出具"该包未被篡改且已评估风险"的证据时调用。

### 用法

入口脚本（在技能目录下执行）：scan_skill.py。

### 流程

1. 触发：识别skill-admission-gate相关任务（见「何时用」）。
2. 执行：按「用法」运行scan_skill.py。
3. 校验：核对脚本输出/退出码是否符合预期。
4. 交付：向用户呈现结果/产物。

> **LGD 三律的可执行实现**：有籍（包指纹）· 有证（扫描证据留痕）· 有门禁（判定与已接受风险须署名）。
> 规则版本 `1.0.0` ｜ 纯标准库 ｜ 离线可跑 ｜ 无需 API key

### 一、为什么需要它

技能生态的安全问题**不是"有没有恶意包"，而是"没有上架闸门"**：

- 技能可以执行任意代码、访问文件系统、发起网络请求——权限面等同于一个本地程序；
- 但其分发形式常看起来像"一段说明文档"，**审查直觉失效**；
- 一旦装上，它就在你的机器上以你的身份运行。

**结论**：技能需要一个**确定性、可留痕、可复核**的安检环节，而不是靠"看起来没问题"。

### 二、什么时候用

| 场景 | 说明 |
|---|---|
| 安装第三方技能前 | 尤其是来源不明、无仓库背书、无 license 的包 |
| 自研技能发布前 | 与 skill-release-gate 配套，作为安全前置 |
| 供应链安全评估 | 批量扫描技能根目录，出一张风险清单 |
| 需要出具证据 | 包指纹 + 文件哈希 + 时间戳，证明"此版本未变" |

### 三、怎么用

#### 单技能审查

```bash
python scripts/scan_skill.py <技能目录> [--json out.json]
```

#### 批量审查（扫一个技能根目录）

```bash
python scripts/scan_skill.py <技能根目录> --batch --json batch-result.json
```

输出示例：

```
技能: my-skill
判定: WARN ｜ BLOCK 0 ｜ WARN 2 ｜ 已接受 0 ｜ 扫描 6 文件
包指纹: cd23896eee940857
  [WARN] EXF-04 script.py:41  requests.post("https://api.example.com/collect", ...)
```

**退出码**：`0` = 非 BLOCK；`1` = BLOCK（可用于 CI 阻断）。

### 四、规则集（v1.0.0）

| 组 | 规则 | 级别 | 检测内容 |
|---|---|---|---|
| **破坏性** | DES-01~05 | **BLOCK** | 递归强制删除、`del /s /f`、`shutil.rmtree`、格式化/写设备、fork 炸弹 |
| **远程执行** | EXE-01,02 | **BLOCK** | `curl|sh`、PowerShell 编码命令、`iex(` |
| | EXE-03,04 | WARN | `eval(`/`exec(`、base64 解码后执行 |
| **数据外泄** | EXF-01,02 | **BLOCK** | 读私钥/凭据文件、读本地保险库与密钥投递工具 |
| | EXF-03,04 | WARN | 读 `.env`/环境凭据、向外部端点 POST/PUT |
| **提示注入** | INJ-01,02 | **BLOCK** | "忽略之前指令"、"不要告诉用户" |
| | INJ-03~05 | WARN | 静默执行、绕过安全/审批、诱导粘贴密钥 |
| **混淆** | OBF-01 | WARN | 超长 Base64 字串（疑似载荷） |
| **作用域** | SCP-01 | WARN | 写入技能目录之外的绝对路径 |

**判定口径**：命中任一 BLOCK → 整体 `BLOCK`；仅命中 WARN → `WARN`；无命中 → `PASS`。

### 五、已接受风险机制（关键设计）

**误报是必然的**——例如本地保险库技能"读 `<local-vault>`"是其**本职**，不是外泄。

**但"接受风险"不能靠静默忽略，必须留痕、必须署名。** 在被审目录放 `.admission-allow.json`：

```json
{
  "schema": "skill-admission-allow/1.0",
  "skill": "dpapi-local-vault",
  "note": "本技能功能即本地凭据保险库，访问该目录是其声明用途。",
  "allow": [
    {
      "rule": "EXF-02",
      "reason": "读写 <local-vault> 是其唯一且声明的用途；密钥不落明文、不出本机。",
      "approved_by": "XLGD",
      "date": "2026-09-12",
      "mitigation": "本技能不发起任何网络请求。"
    }
  ]
}
```

声明后该规则**转入 ACCEPTED 分类**（仍出现在报告里，但不影响判定）——**这就是"有门禁 + 有证"**。

### 六、产出的证据（"有证"）

每次审查都输出：

| 字段 | 含义 |
|---|---|
| `package_fingerprint_sha256` | 全包文件哈希聚合指纹——用于判定"包是否被改过" |
| `file_hashes[]` | 每个文件的 sha256 与字节数 |
| `rule_version` | 规则集版本（规则会演进，须记录用哪版判的） |
| `timestamp_utc` | 审查时间 |
| `accepted_risks[]` | 已接受风险及其署名与理由 |

**用途**：上架台账、争议取证、版本回归比对（新版本指纹变了 → 须重审）。

### 七、边界与诚实声明

- **模式匹配有极限**：本工具查的是**已知模式**，能拦住粗糙与常见手法，**不能替代人工代码审计**；对高度混淆、逻辑后门、依赖链投毒（第三方库）覆盖不足。
- **不做沙箱执行**：只做**静态审查**，不运行动态行为分析。
- **规则会演进**：判定依赖 `rule_version`；跨版本比较结论时须对齐规则版本。
- **不构成安全保证**：`PASS` 表示"未命中本规则集"，**不等于"安全"**。

### 八、与 LGD 的对应

| LGD 法则 | 本技能的实现 |
|---|---|
| **有籍（Registry）** | 包指纹 + 文件哈希：这个包"是谁、是什么版本"可唯一标识 |
| **有证（Evidence）** | 扫描发现 + 规则版本 + 时间戳，全部落盘 JSON |
| **有门禁（Gates）** | BLOCK 则阻断（退出码 1）；接受风险须署名 + 给理由 + 给缓解措施 |

### 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「这个第三方技能装了安全吗」 / "is this third-party skill safe to install"
- 「安装前先扫一遍有没有后门」 / "scan for backdoors before I install"
- 「帮我看这里面有没有木马」 / "check this plugin for hidden payloads"
- 「自研插件发布前要过安检」 / "we need a pre-release security check"
- 「供应链评估怎么拿出证据」 / "how do we evidence a supply chain review"
- 「提示注入藏在说明文件里」 / "prompt injection hidden in the docs"

Trigger when the user says any of the above, in Chinese or English.

---

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/skill-admission-gate
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/skill-admission-gate/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
