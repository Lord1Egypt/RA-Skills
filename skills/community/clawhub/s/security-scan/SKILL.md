---
name: security-scan
description: Security review workflow for OpenClaw skills and other small code folders. Use when auditing a skill before publishing or installing it, checking for dangerous code patterns, possible hardcoded secrets, risky file permissions, or lightweight supply-chain concerns. Best for quick static review and cautious go/no-go recommendations, not full malware analysis or sandbox forensics.
---

# Security Scan

Perform a lightweight security review before trusting, publishing, or installing a skill.

## What this skill does

Use this skill to:
- inspect a skill directory for obviously dangerous code patterns
- look for likely hardcoded credentials or tokens
- flag risky file permissions
- produce a concise risk summary with recommended next steps

This skill is intentionally conservative and lightweight. Treat findings as review signals, not proof of compromise.

## What this skill does not do

Do not claim capabilities that are not present in the bundled resources.

This skill does **not** provide:
- true sandbox execution
- system call tracing
- network traffic capture
- dependency CVE resolution from external databases
- automatic approval or rejection logic

If deeper reverse engineering or threat analysis is needed, do a manual review and use stronger external tooling.

## Bundled resource

### `scripts/scan.sh`

Run the included shell scanner for a quick static pass:

```bash
bash scripts/scan.sh /path/to/target
```

The script currently checks for:
- suspicious function names such as `eval(`, `exec(`, `system(`, and `spawn(`
- simple hardcoded-secret patterns
- world-writable files

Because the script uses grep-style heuristics, expect both false positives and false negatives.

## Recommended workflow

### 1. Scope the review

Confirm what you are reviewing:
- target directory
- whether it is a skill, script bundle, or general code folder
- whether the goal is publish review, install review, or a quick sanity check

### 2. Run the quick scan

From the skill directory:

```bash
bash scripts/scan.sh /path/to/target
```

If the target is the current directory:

```bash
bash scripts/scan.sh .
```

### 3. Review the findings manually

Do not stop at raw matches. Inspect the surrounding code and decide whether each finding is:
- expected and justified
- suspicious but explainable
- high-risk and likely unacceptable

Pay special attention to:
- shell execution that touches untrusted input
- outbound network access
- credential handling
- writes outside the working directory
- self-modifying or persistence-oriented behavior

### 4. Give a practical verdict

Summarize the result in plain language using a simple rubric:
- **Low risk:** no meaningful issues found in this lightweight review
- **Needs review:** suspicious patterns or ambiguous findings require manual inspection before trust
- **High risk:** clear dangerous behavior, likely secrets, or unjustified execution patterns

### 5. Recommend next actions

Examples:
- publish/install as-is
- publish/install only after removing a flagged pattern
- rotate exposed credentials
- request source clarification from the author
- escalate to deeper manual or sandboxed analysis

## Reporting pattern

Use a compact structure like this:

```text
Security scan summary
- Target: <path>
- Result: Low risk | Needs review | High risk
- Findings:
  - <finding 1>
  - <finding 2>
- Confidence: Low | Medium | High
- Recommended action: <next step>
```

## Triage guidance

### Usually high risk
- obvious credential material checked into the repo
- hidden or unjustified command execution
- code that downloads and runs remote content
- writes to sensitive locations without a clear reason

### Usually medium risk
- use of shell execution with unclear input handling
- overly broad file permissions
- suspicious obfuscation or encoded payloads
- installer/update logic that is hard to verify quickly

### Usually low risk
- benign matches in docs or examples
- helper scripts that use shell commands in a narrow, understandable way
- false positives from regex scanning

## Practical cautions

- Prefer a short, evidence-based verdict over dramatic claims.
- Quote the matched lines or file paths when useful.
- If confidence is low, say so explicitly.
- Do not claim the scan is comprehensive.
- For publish decisions, err on the side of requiring cleanup when the skill still contains templates, TODOs, placeholder claims, or unverified commands.
