---
name: text-replace
description: 跨文件批量替换 — 多文件批量查找替换（字面量/正则），默认统计命中不写盘 --apply 才改，改前自动 .bak 备份（零依赖） 适用场景：当需要跨文件批量替换能力时使用本技能；触发词：text-replace。
slug: text-replace
title: text-replace
version: 1.0.1
display_name: 跨文件批量替换
display_name_en: Bulk Text Replace
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
category: 效率工具
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
copyright: SynomosAI
description_zh: "跨文件批量替换 — 多文件批量查找替换（字面量/正则），默认统计命中不写盘 --apply 才改，改前自动 .bak 备份（零依赖）"
description_en: "Bulk find and replace across files (literal or regex); counts hits without writing by default, --apply writes with automatic .bak backups (zero-dependency)."
read_when:
  - 跨多个文件批量改名/改版本号/改接口地址
  - 需要先预览命中、确认后再写盘的批量替换
  - 正则批量替换且要求自动 .bak 回滚
  - 机器可读 JSON 输出（--json）接入自有流程
classification:
  skillhub: ["productivity"]
  iso_25010: ["Maintainability", "Usability"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
tags: [text-replace, 效率工具]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/text_replace.py
  runtime: python3
  call_pattern: args
input_schema:
  glob:
    type: string
    description: "glob"
    required: true
  old:
    type: string
    description: "old"
    required: true
  new:
    type: string
    description: "new"
    required: true
  regex:
    type: bool
    description: "按正则解释 old"
    required: false
  apply:
    type: bool
    description: "写入（缺省只统计；写入前每文件生成 .bak）"
    required: false
  json:
    type: bool
    description: "json"
    required: false
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - text
  - replace
  - bulk
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

**text-replace** v1.0.1 · LGD-Powered productivity family · zero-dependency

### The pain
Renaming / bumping versions / changing API hosts — opening dozens of files one by one until your eyes burn.

### When to use
When the user needs bulk find-and-replace across files.

### Usage
```bash
python scripts/text_replace.py --help
```
- Success → rc=0; findings → rc=1; usage error → rc=2
- `--json` for machine-readable output
- Writing operations default to **dry-run preview**; add `--apply` to execute (a .bak backup is made per file first)

### Workflow
1. Trigger: identify a bulk text-replace task (see When to use).
2. Execute: run text_replace.py per Usage.
3. Verify: check output / exit code against expectations.
4. Deliver: present results / artifacts.

### Safety design
- Moves / renames only; never deletes content files.
- Auto-backup before writing (text-replace writes a .bak; rollback is available).

### LGD-Powered
This is an LGD Three-Laws productivity-family piece: high-frequency file operations made **previewable, rollback-able, traceable** deterministic tools.

### Disclaimer
Efficiency aid; back up important data and preview before --apply.

## 中文

**text-replace** v1.0.1 · LGD-Powered 效率工具家族 · 零依赖

### 痛点
改名/改版本号/改接口地址，几十个文件一个个开编辑器改到眼瞎

### 何时用
- 当用户需要跨文件批量替换相关能力时。

### 用法
```bash
python scripts/text_replace.py --help
```
- 成功 → rc=0；发现问题 → rc=1；用法错误 → rc=2
- 支持 `--json` 机器可读输出
- 涉及写盘的操作默认 **dry-run 预览**，加 `--apply` 才执行（写盘前自动 .bak 备份）

### 流程
1. 触发：识别跨文件批量替换相关任务（见「何时用」）。
2. 执行：按「用法」运行text_replace.py。
3. 校验：核对脚本输出/退出码是否符合预期。
4. 交付：向用户呈现结果/产物。

### 安全设计
- 只替换内容，不删除文件。
- 写盘前自动备份（生成 .bak，可回滚）。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

### 免责
本工具为效率辅助；对重要数据请先备份并在预览确认后再 --apply。
