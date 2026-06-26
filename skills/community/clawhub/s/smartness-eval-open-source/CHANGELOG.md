# Changelog / 版本变更日志

All notable changes to this project are documented in this file.
本文件记录所有重要变更。

Format follows [Keep a Changelog](https://keepachangelog.com/).

---

## [0.3.3] - 2026-03-22

### Breaking Changes / 重大变更
- **Complete architecture rewrite** — Replaced 14-dimension mixed-signal scoring with clean 3-layer architecture: Functional Tests (70%) + System Health (20%) + Growth (10%).
  完全重写评分架构：三层设计（功能测试70% + 系统健康20% + 成长进化10%）。
- **Version-agnostic tests** — All functional tests now use `cognitive-kernel-v6.py --process` as single entry point. Removed all hardcoded `message-analyzer-v5.py` calls that broke on every version upgrade.
  版本无关测试：所有功能测试统一走 kernel --process，移除导致每次升级分数下滑的硬编码V5脚本调用。
- **New 11 dimensions** — `intent_understanding`, `safety_awareness`, `task_routing`, `response_quality`, `robustness`, `latency`, `error_control`, `infrastructure`, `knowledge`, `self_improvement`, `pattern_learning`.
  新11维度评分体系。

### Added / 新增
- **`--workspace` flag** — Override workspace path for standalone usage.
  新增 `--workspace` 参数支持独立运行。
- **Auto workspace discovery** — Detects workspace via `OPENCLAW_WORKSPACE` env, installed-skill parent, or `~/.openclaw/workspace` default.
  自动发现工作目录。
- **30 capability tests** — Intent recognition (7), safety awareness (6), task routing (5), response quality (5), robustness (4), infrastructure (4).
  30项能力测试覆盖6个功能维度。
- **Health metrics from V6+ state files** — Reads kernel log DB, error-tracker, healing-log, cron-governor for real system health.
  从V6+状态文件采集健康指标。
- **Growth metrics** — Tracks reasoning store, memory index, reflection reports, rule candidates, pattern library, auto-rules.
  成长指标追踪。

### Removed / 移除
- **Anti-gaming probes** — Removed randomized probe tests that used deprecated `message-analyzer-v5.py`.
  移除使用过期脚本的反作弊探针。
- **Mixed-signal scoring** — Removed arbitrary metric blending (e.g., duplicate_reply_rate affecting analysis score).
  移除无关指标混合评分。
- **Fallback scores** — No more `ts_or('dim', 60)` masking missing data with fake scores.
  移除虚假兜底分数。

### Fixed / 修复
- **Score drops on upgrade** — Root cause was hardcoded V5 script paths in tests. Now all tests use the current kernel.
  修复每次升级导致分数下滑的根本原因。
- **Proxy metrics** — Each dimension now scored by directly relevant evidence only.
  每个维度仅由直接相关的证据评分。

---

## [0.2.1] - 2026-03-16

### Added / 新增
- **`scripts/state_probe.py`** — New safe probe script replacing inline `python -c` commands. Supports three probes: `quality-gate-prompt`, `latency-state-count`, `rule-candidates`.
  新增安全探针脚本，替代内联 `python -c` 命令。支持三种探针。
- **Command validation** (`validate_command()` in `eval.py`) — Multi-layer security gate before any subprocess execution: interpreter whitelist, inline code block, absolute path block, path traversal block, prefix whitelist.
  多层命令安全校验：解释器白名单、内联代码阻止、绝对路径阻止、路径穿越阻止、前缀白名单。

### Changed / 变更
- **Task suite** — Replaced all `python -c` + `exec(open(...).read())` patterns in `config/task-suite.json` with calls to `state_probe.py`. Removed all hardcoded absolute paths (`/Users/...`).
  替换所有内联代码执行和硬编码绝对路径。
- **Author** — Updated metadata author to `圆规` across `_meta.json`, `SKILL.md`, `LICENSE`.
  作者更新为"圆规"。
- **LLM judge docs** — Clarified that `--llm-judge` is off by default and requires explicit opt-in + API key. No raw data is sent externally.
  明确说明 LLM 裁判功能默认关闭。

### Security / 安全
- Blocked unsafe command patterns: `-c` flag, `exec(` string, absolute paths, `..` traversal, non-whitelisted path prefixes.
  阻止不安全命令模式。
- All test commands now pass through `validate_command()` before `subprocess.run()`.
  所有测试命令执行前必须通过安全校验。

---

## [0.2.0] - 2026-03-16

### Added / 新增
- **12-dimension evaluation framework** — Understanding, Analysis, Thinking, Reasoning, Self-iteration, Dialogue, Responsiveness + Robustness, Generalization, Policy adherence, Tool reliability, Calibration.
  12 维度评估框架。
- **28 automated tests** — Covering intent recognition, risk detection, reasoning templates, API health, cron status, benchmark pass rate, and more.
  28 项自动化测试。
- **3 evaluation modes** — `quick` (daily), `standard` (weekly), `deep` (monthly audit with pass@k).
  三种评估模式。
- **Anti-gaming probes** — Randomized test inputs injected at eval time to prevent overfitting.
  反作弊随机探针。
- **Trend comparison** — `--compare-last` flag to show dimension-level deltas vs previous run.
  趋势对比功能。
- **Optional LLM judge** — `--llm-judge` for subjective scoring via DeepSeek or OpenAI API.
  可选 LLM 裁判功能。
- **Structured output** — JSON run file, Markdown report, and JSONL history for longitudinal analysis.
  结构化输出：JSON、Markdown、JSONL 历史。
- **Detailed rubrics** — 0–5 scale with concrete criteria for all 12 dimensions in `config/rubrics.json`.
  详细评分量表。
- **Health check** — `scripts/check.py` for verifying skill structure integrity.
  技能结构健康检查。
