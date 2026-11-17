---
name: regex-sandbox
description: 正则沙盒 — 正则即写即测：匹配/分组捕获/替换预览/标志位，无匹配给 rc=1，调正则不用来回跑脚本（零依赖） 适用场景：当需要正则沙盒能力时使用本技能；触发词：regex-sandbox。
slug: regex-sandbox
title: 正则沙盒
version: 1.0.1
display_name: 正则沙盒
display_name_en: Regex Sandbox
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write
category: 效率工具
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
copyright: SynomosAI
description_zh: "正则沙盒 — 正则即写即测：匹配/分组捕获/替换预览/标志位，无匹配给 rc=1，调正则不用来回跑脚本（零依赖）"
description_en: "Write-and-test regex sandbox: matching, group capture, replace preview and flags; rc=1 on no-match so tuning does not need script reruns (zero-dependency)."
read_when:
  - 要写/调正则表达式但不想反复改代码重跑
  - 需要实时预览匹配、分组捕获与替换效果
  - 要确认正则在目标文本上是否命中
  - 想用机器可读 JSON 输出比对正则结果
classification:
  skillhub: ["productivity"]
  iso_25010: ["Maintainability", "Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [regex-sandbox, 效率工具, 正则, 测试]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/regex_sandbox.py
  runtime: python3
  call_pattern: args
input_schema:
  pattern:
    type: string
    description: "pattern"
    required: true
  text:
    type: string
    description: "待测文本（缺省读 stdin）"
    required: false
  file:
    type: string
    description: "从文件读文本"
    required: false
  replace:
    type: string
    description: '替换模板（如 <b>\1</b>）'
    required: false
  flags:
    type: string
    description: "flags"
    required: false
  json:
    type: bool
    description: "json"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - regex
  - sandbox
  - testing
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

**regex-sandbox** v1.0.1 · LGD-Powered productivity family · zero-dependency

### Pain point
Tuning regex used to mean editing code and rerunning — one wrong pattern cost half a day of debugging.

### When to use
- Whenever the user needs regex-sandbox capabilities.

### Usage
```bash
python scripts/regex_sandbox.py --help
```
- Success → rc=0; problem found → rc=1; usage error → rc=2
- `--json` for machine-readable output
- Disk-writing operations default to **dry-run preview**; add `--apply` to execute (text-replace / dup-finder also back up first)

### Workflow
1. Trigger: identify a regex-sandbox task (see When to use).
2. Execute: run regex_sandbox.py per Usage.
3. Verify: check script output / exit code against expectations.
4. Deliver: present the result / artifact to the user.

### Safety design
- Only moves/renames, never deletes content files (dup-finder `--apply` deletes only the byte-identical duplicate of the first copy)
- Auto-backup before disk writes (text-replace generates .bak; batch-renamer / organizer can log the plan via `--json` for rollback)

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once produced)
- Version: 1.0.1
- Safety: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

### Disclaimer
This is a productivity helper; back up important data and confirm the preview before `--apply`.

## 中文

**regex-sandbox** v1.0.1 · LGD-Powered 效率工具家族 · 零依赖

### 痛点
调正则全靠改代码重跑，写错一次 debug 半天

### 何时用

- 当用户需要正则沙盒相关能力时。

### 用法
```bash
python scripts/regex_sandbox.py --help
```
- 成功 → rc=0；发现问题 → rc=1；用法错误 → rc=2
- 支持 `--json` 机器可读输出
- 涉及写盘的操作默认 **dry-run 预览**，加 `--apply` 才执行（text-replace/dup-finder 还会先备份）

### 流程

1. 触发：识别正则沙盒相关任务（见「何时用」）。
2. 执行：按「用法」运行 regex_sandbox.py。
3. 校验：核对脚本输出/退出码是否符合预期。
4. 交付：向用户呈现结果/产物。

### 安全设计
- 只移动/重命名，不删除内容文件（dup-finder 的 --apply 仅删除与首个完全同哈希的副本）
- 写盘前自动备份（text-replace 生成 .bak；batch-renamer/organizer 可用 --json 记录计划回滚）

### 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

### 免责
本工具为效率辅助；对重要数据请先备份并在预览确认后再 --apply。
