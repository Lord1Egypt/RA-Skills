---
name: ai-engineering-os
description: >
  A unified AI Engineering Operating System that orchestrates the full lifecycle
  of agent creation - extracting tacit knowledge, structuring the Agent OS, and
  enforcing pre-deployment governance. Use this skill to build production-ready,
  context-aware agents that are immune to AI Execution Hallucination and the
  Expertise Paradox.
---

# AI Engineering Operating System (The Unified Architecture)

This skill represents a paradigm shift from "Prompt Engineering" to "Knowledge Engineering." It combines three foundational capabilities — Tacit Knowledge Extraction, Agent OS Architecture, and Anti-Micromanagement Governance — into a single, self-improving cognitive architecture.

## The Six Paradigm Shifts

1. **From Prompt Engineering to Knowledge Engineering**: The prompt is the last step. The real work is upstream extraction and structuring.
2. **From Agent as Tool to Agent as Apprentice**: The agent interviews the master (SECI model), learns the craft, and operates under supervision.
3. **From Trust by Default to Trust by Proof**: Trust is an engineering artifact earned through the Mandatory Proof of Action Protocol.
4. **From One-Shot to Living Configuration**: The agent's OS is a living document that evolves through continuous feedback.
5. **From Automation to Augmented Cognition**: Human judgment and agent capability are structurally interleaved.
6. **From Scaling Agents to Scaling Intent**: You are not scaling compute; you are scaling the human's extracted judgment.

---

## The Unified Workflow

When tasked with building or deploying a new AI agent, execute this three-phase pipeline:

### Phase 1: The Extraction Interview (Tacit Knowledge Extractor)

Do not accept vague prompts. Ask the user for a concrete past example of the task. Conduct a structured interview using the SECI Externalization Interview Framework below to map workflows, decision rules, and edge cases. Synthesize the answers into a Tacit Knowledge Profile.

**Crucial Step: You must pause and ask the user to confirm the synthesis before proceeding.**

### Phase 2: The OS Build (Agent OS Builder)

Convert the confirmed Tacit Profile into a structured, version-controllable file system. Generate the five core OS files: SOUL.md, AGENTS.md, USER.md, HEARTBEAT.md, and TOOLS.md using the Agent OS Architecture Guide below.

### Phase 3: The Pre-Deployment Audit (Anti-Micromanagement Guard)

Before the agent is allowed to execute tasks, enforce the Pre-Deployment Governance Checklist below. Ensure the agent is configured to follow the **Mandatory Proof of Action Protocol**: every completion claim must include an exact file path, actual content confirmation, and a timestamp. Use the Verify Action Script to validate the agent's output.

---

## The Self-Improving Feedback Loop

This unified system learns from its own deployments. After every full cycle:

1. **Extraction Loop**: Did the user have to correct the synthesis in Phase 1? If yes, update the interview framework with better probing questions.
2. **Architecture Loop**: Were any OS files missing necessary context in Phase 2? If yes, update the OS templates.
3. **Governance Loop**: Did the agent attempt to hallucinate execution in Phase 3? If yes, strengthen the governance checklist.

---
---

# REFERENCE: SECI Externalization Interview Framework

This framework provides the structured interview questions for extracting tacit knowledge from domain experts. It is organized by the Nonaka SECI model's "Externalization" phase — converting unconscious judgment into explicit, machine-readable rules.

## Interview Protocol

Ask ONE question at a time. Wait for the answer before proceeding. Never ask more than 2 follow-ups on the same topic.

### Round 1: Workflow Mapping (The "What")

| # | Question | Purpose |
|---|----------|---------|
| 1 | "Walk me through the last time you did this task from start to finish." | Captures the full workflow sequence |
| 2 | "What tools or systems did you use at each step?" | Maps the tool chain |
| 3 | "How long does each step typically take?" | Establishes time expectations |
| 4 | "What information do you need before you can start?" | Identifies input dependencies |

### Round 2: Decision Points (The "Why")

| # | Question | Purpose |
|---|----------|---------|
| 5 | "At what point in the process do you have to make a judgment call?" | Identifies decision nodes |
| 6 | "What signals tell you to choose option A over option B?" | Extracts decision heuristics |
| 7 | "What does a 'good' result look like vs. a 'bad' one?" | Defines quality criteria |
| 8 | "How do you know when you're done?" | Establishes completion criteria |

### Round 3: Edge Cases and Exceptions (The "What If")

| # | Question | Purpose |
|---|----------|---------|
| 9 | "What's the most common thing that goes wrong?" | Identifies failure modes |
| 10 | "When something goes wrong, what do you do?" | Captures recovery procedures |
| 11 | "Are there situations where you break your own rules?" | Surfaces hidden exceptions |
| 12 | "What would a new hire get wrong on their first attempt?" | Reveals non-obvious pitfalls |

### Round 4: Context and Preferences (The "How")

| # | Question | Purpose |
|---|----------|---------|
| 13 | "What tone or style do you use?" | Captures voice and communication norms |
| 14 | "Who do you communicate with during this task?" | Maps stakeholder relationships |
| 15 | "What's your preferred format for the output?" | Defines output specifications |
| 16 | "Is there anything you always do that others might consider optional?" | Surfaces personal best practices |

### Synthesis Rules

After completing the interview:

1. Group answers into: **Workflow Steps**, **Decision Rules**, **Edge Cases**, and **Preferences**.
2. Write each decision rule as an IF/THEN statement.
3. Write each edge case as a WHEN/THEN exception.
4. Present the synthesis to the user and ask: "Did I capture your decision-making process correctly?"
5. Do NOT proceed until the user confirms.

---
---

# REFERENCE: Agent OS Architecture Guide

This guide defines the structure and purpose of each file in the Agent OS. Each file serves a distinct function and must not overlap with others.

## File Architecture

| File | Purpose | Analogy | Source of Truth |
|------|---------|---------|-----------------|
| SOUL.md | Personality, values, tone, behavioral boundaries | Character sheet | Tacit Profile: Communication Preferences |
| AGENTS.md | Step-by-step workflows and operating procedures | Operating manual | Tacit Profile: Workflow Steps + Decision Rules |
| USER.md | User profile, preferences, schedule, communication style | Employee handbook | Tacit Profile: Communication Preferences + Quality Criteria |
| HEARTBEAT.md | Periodic task checklist (cron-like recurring tasks) | Daily standup agenda | Tacit Profile: Workflow Steps (recurring) |
| TOOLS.md | Authorized tools and their usage constraints | Toolbox inventory | Tacit Profile: Workflow Steps (tools column) |

## File Generation Rules

### SOUL.md

Extract from the Tacit Profile's "Communication Preferences" and "Personal Best Practices" sections.

```markdown
# Soul
## Identity
[Who this agent is and what it stands for]
## Tone
[Communication style: formal/casual, direct/diplomatic, etc.]
## Boundaries
[What this agent will NOT do, ethical guardrails]
## Values
[What this agent prioritizes when making trade-offs]
```

### AGENTS.md

Extract from the Tacit Profile's "Workflow Steps" and "Decision Rules" sections.

```markdown
# Operating Manual
## Workflow: {{TASK_NAME}}
### Step 1: {{STEP}}
[Detailed instructions]
### Decision Point: {{DECISION}}
IF {{CONDITION}} THEN {{ACTION}}
### Edge Case: {{EXCEPTION}}
WHEN {{TRIGGER}} THEN {{RESPONSE}}
```

### USER.md

Extract from the Tacit Profile's "Communication Preferences" and "Quality Criteria" sections.

```markdown
# User Profile
## Name: {{USER_NAME}}
## Role: {{ROLE}}
## Preferences
[Schedule, communication channels, output format preferences]
## Quality Standards
[What "good" looks like, what "done" means]
```

### HEARTBEAT.md

Extract from the Tacit Profile's recurring workflow steps.

```markdown
# Heartbeat
## Daily
- [ ] {{DAILY_TASK_1}}
- [ ] {{DAILY_TASK_2}}
## Weekly
- [ ] {{WEEKLY_TASK_1}}
## Monthly
- [ ] {{MONTHLY_TASK_1}}
```

### TOOLS.md

Extract from the Tacit Profile's "Tools Used" column in workflow steps.

```markdown
# Authorized Tools
## {{TOOL_NAME}}
- Purpose: {{PURPOSE}}
- Access Level: {{READ/WRITE/EXECUTE}}
- Constraints: {{LIMITS}}
```

## Validation Checklist

After generating all files, verify:

1. Every workflow step from the Tacit Profile is represented in AGENTS.md.
2. Every decision rule is an explicit IF/THEN in AGENTS.md.
3. Every edge case is a WHEN/THEN exception in AGENTS.md.
4. SOUL.md tone matches the Tacit Profile's communication preferences.
5. TOOLS.md lists only tools mentioned in the Tacit Profile.
6. No information is duplicated across files.

---
---

# REFERENCE: Pre-Deployment Governance Checklist

This checklist must be completed before any agent is deployed to production. It is based on the OWASP Top 10 for Agentic Applications (Dec 2025), the Scrum.org Definition of Done for AI Agents (Jan 2026), and the Mandatory Proof of Action Protocol.

## Section 1: Proof of Action Protocol

| # | Check | Pass Criteria | Status |
|---|-------|---------------|--------|
| 1.1 | Agent provides exact file path for every write action | Absolute path returned, file exists at path | [ ] |
| 1.2 | Agent provides content confirmation (tail -n 3) | Content matches expected output | [ ] |
| 1.3 | Agent provides timestamp for every action | Timestamp is within acceptable range | [ ] |
| 1.4 | Agent explicitly reports failure when proof is missing | No synthesized confirmations detected | [ ] |

## Section 2: Golden Dataset Accuracy

| # | Check | Pass Criteria | Status |
|---|-------|---------------|--------|
| 2.1 | Golden Dataset exists (50-100 curated inputs) | Dataset file present and validated | [ ] |
| 2.2 | Agent tested against Golden Dataset | Test run completed | [ ] |
| 2.3 | Semantic similarity score >90% | ROUGE or Cosine Similarity above threshold | [ ] |
| 2.4 | Failure cases documented | Each failure has root cause analysis | [ ] |

## Section 3: Security Guardrails

| # | Check | Pass Criteria | Status |
|---|-------|---------------|--------|
| 3.1 | PII redaction active | Test PII input is redacted to [REDACTED] | [ ] |
| 3.2 | Least-privilege access enforced | Agent has only minimum required permissions | [ ] |
| 3.3 | Input validation active | Malformed inputs are rejected gracefully | [ ] |
| 3.4 | Output validation active | Outputs conform to expected schema | [ ] |

## Section 4: Cost and Loop Protection

| # | Check | Pass Criteria | Status |
|---|-------|---------------|--------|
| 4.1 | Circuit breaker configured | Max steps per task defined (default: 5) | [ ] |
| 4.2 | Cost cap configured | Max spend per execution defined (default: $2) | [ ] |
| 4.3 | Timeout configured | Max execution time defined | [ ] |
| 4.4 | Infinite loop detection active | Repeated identical actions trigger halt | [ ] |

## Section 5: Human Fallback

| # | Check | Pass Criteria | Status |
|---|-------|---------------|--------|
| 5.1 | Confidence threshold defined | Default: 70% | [ ] |
| 5.2 | Fallback routing configured | Low-confidence queries route to human | [ ] |
| 5.3 | Escalation path documented | Clear chain of responsibility defined | [ ] |
| 5.4 | Stop conditions documented | Conditions that trigger full agent halt | [ ] |

## Section 6: Post-Deployment Monitoring

| # | Check | Pass Criteria | Status |
|---|-------|---------------|--------|
| 6.1 | Audit logging enabled | Every action logged with who/what/when/where | [ ] |
| 6.2 | Drift detection scheduled | Weekly re-test against Golden Dataset | [ ] |
| 6.3 | Ownership assigned | Named human DRI for the live agent | [ ] |
| 6.4 | Incident response plan documented | Steps for rollback, investigation, fix | [ ] |

## Scoring

Each section is scored Pass/Fail. All 6 sections must pass for deployment approval. A single failed check in Sections 1-3 (critical) blocks deployment. Failed checks in Sections 4-6 (important) require documented risk acceptance from the DRI.

---
---

# SCRIPT: Verify Action — Mandatory Proof of Action Protocol

Validates that an agent's claimed action actually occurred. This is the enforcement mechanism for the Anti-Micromanagement Guard. Instead of building "auditor agents" to watch other agents, this script provides deterministic, verifiable proof.

## Purpose

Every time an agent claims "Done," this script runs three checks to verify the claim is real and not an "AI Execution Hallucination" — a documented failure mode where agents confidently report completing actions they never took.

## The Three Verification Checks

| # | Check | What It Validates | Failure Meaning |
|---|-------|-------------------|-----------------|
| 1 | **File Exists** | Does the file exist at the claimed path? | Action was likely hallucinated entirely |
| 2 | **Content Match** | Does the file contain the expected content substring? | Agent wrote wrong data or a placeholder |
| 3 | **Timestamp Fresh** | Was the file modified within the allowed time window? | Agent is referencing a stale pre-existing file |

## Usage

```bash
python verify_action.py --path <file_path> --expected <expected_content> [--max-age <seconds>]
```

**Parameters:**

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| --path | Yes | — | File path the agent claims to have written |
| --expected | Yes | — | Expected content substring to verify |
| --max-age | No | 300 | Maximum file age in seconds |

**Exit Codes:**
- 0 — All checks passed. Action verified.
- 1 — One or more checks failed. Action NOT verified.

## Output Format

The script prints a JSON report to stdout:

```json
{
  "verification_time": "2026-04-15T10:54:09.462914",
  "claimed_path": "/path/to/file.txt",
  "overall_verdict": "PASS — Action verified",
  "checks": [
    {
      "check": "file_exists",
      "path": "/path/to/file.txt",
      "passed": true,
      "detail": "File found"
    },
    {
      "check": "content_match",
      "passed": true,
      "tail_3_lines": ["line1", "line2", "line3"],
      "detail": "Content verified"
    },
    {
      "check": "timestamp_fresh",
      "passed": true,
      "file_modified": "2026-04-15T10:53:58.278625",
      "age_seconds": 11.2,
      "max_age_seconds": 300,
      "detail": "File modified 11.2s ago"
    }
  ]
}
```

## Source Code

```python
#!/usr/bin/env python3
"""
Verify Action Script — Mandatory Proof of Action Protocol
Validates that an agent's claimed action actually occurred.

Usage:
    python verify_action.py --path <file_path> --expected <expected_content> [--max-age <seconds>]

Returns:
    Exit code 0 if all checks pass, exit code 1 if any check fails.
    Prints a JSON report with pass/fail status for each check.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime


def verify_file_exists(file_path: str) -> dict:
    """Check 1: Does the file exist at the claimed path?"""
    exists = os.path.isfile(file_path)
    return {
        "check": "file_exists",
        "path": file_path,
        "passed": exists,
        "detail": "File found" if exists else "FILE NOT FOUND — action likely hallucinated"
    }


def verify_content(file_path: str, expected_content: str) -> dict:
    """Check 2: Does the file contain the expected content?"""
    if not os.path.isfile(file_path):
        return {
            "check": "content_match",
            "passed": False,
            "detail": "Cannot verify content — file does not exist"
        }
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            actual = f.read()
        match = expected_content.strip() in actual
        tail_lines = actual.strip().split("\n")[-3:]
        return {
            "check": "content_match",
            "passed": match,
            "tail_3_lines": tail_lines,
            "detail": "Content verified" if match else "CONTENT MISMATCH — agent may have written wrong data"
        }
    except Exception as e:
        return {
            "check": "content_match",
            "passed": False,
            "detail": f"Error reading file: {str(e)}"
        }


def verify_timestamp(file_path: str, max_age_seconds: int = 300) -> dict:
    """Check 3: Was the file modified recently (within max_age_seconds)?"""
    if not os.path.isfile(file_path):
        return {
            "check": "timestamp_fresh",
            "passed": False,
            "detail": "Cannot verify timestamp — file does not exist"
        }
    try:
        mtime = os.path.getmtime(file_path)
        age = time.time() - mtime
        fresh = age <= max_age_seconds
        return {
            "check": "timestamp_fresh",
            "passed": fresh,
            "file_modified": datetime.fromtimestamp(mtime).isoformat(),
            "age_seconds": round(age, 1),
            "max_age_seconds": max_age_seconds,
            "detail": f"File modified {round(age, 1)}s ago" if fresh else f"FILE STALE — modified {round(age, 1)}s ago (max: {max_age_seconds}s)"
        }
    except Exception as e:
        return {
            "check": "timestamp_fresh",
            "passed": False,
            "detail": f"Error checking timestamp: {str(e)}"
        }


def run_verification(file_path: str, expected_content: str, max_age: int) -> dict:
    """Run all three verification checks and produce a report."""
    checks = [
        verify_file_exists(file_path),
        verify_content(file_path, expected_content),
        verify_timestamp(file_path, max_age)
    ]
    all_passed = all(c["passed"] for c in checks)
    report = {
        "verification_time": datetime.now().isoformat(),
        "claimed_path": file_path,
        "overall_verdict": "PASS — Action verified" if all_passed else "FAIL — Action NOT verified",
        "checks": checks
    }
    return report


def main():
    parser = argparse.ArgumentParser(description="Verify agent action proof")
    parser.add_argument("--path", required=True, help="File path the agent claims to have written")
    parser.add_argument("--expected", required=True, help="Expected content substring")
    parser.add_argument("--max-age", type=int, default=300, help="Max file age in seconds (default: 300)")
    args = parser.parse_args()

    report = run_verification(args.path, args.expected, args.max_age)
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["overall_verdict"].startswith("PASS") else 1)


if __name__ == "__main__":
    main()
```

## Integration

When using this script within the AI Engineering OS workflow, call it at the end of Phase 3 (Pre-Deployment Audit) for every file the agent claims to have created or modified. If any check fails, the agent's action is rejected and must be re-executed.

---
---

# TEMPLATE: Tacit Knowledge Profile

## Tacit Knowledge Profile: {{TASK_NAME}}

**Extracted from**: {{USER_NAME}}
**Date**: {{DATE}}
**Domain**: {{DOMAIN}}

### Workflow Steps

| Step | Action | Tools Used | Duration | Input Required |
|------|--------|-----------|----------|----------------|
| 1 | {{STEP_1}} | {{TOOLS_1}} | {{TIME_1}} | {{INPUT_1}} |
| 2 | {{STEP_2}} | {{TOOLS_2}} | {{TIME_2}} | {{INPUT_2}} |

### Decision Rules

| # | Condition (IF) | Action (THEN) | Confidence |
|---|----------------|---------------|------------|
| 1 | {{CONDITION_1}} | {{ACTION_1}} | {{CONF_1}} |
| 2 | {{CONDITION_2}} | {{ACTION_2}} | {{CONF_2}} |

### Edge Cases and Exceptions

| # | Trigger (WHEN) | Response (THEN) | Frequency |
|---|----------------|-----------------|-----------|
| 1 | {{TRIGGER_1}} | {{RESPONSE_1}} | {{FREQ_1}} |
| 2 | {{TRIGGER_2}} | {{RESPONSE_2}} | {{FREQ_2}} |

### Communication Preferences

**Tone**: {{TONE}}
**Style**: {{STYLE}}
**Output Format**: {{FORMAT}}
**Stakeholders**: {{STAKEHOLDERS}}

### Quality Criteria

**Good Output Looks Like**: {{GOOD_OUTPUT}}
**Bad Output Looks Like**: {{BAD_OUTPUT}}
**Completion Signal**: {{DONE_SIGNAL}}

### Personal Best Practices

{{BEST_PRACTICES}}

---

*This profile is generated by Phase 1 (Extraction Interview) and serves as the single source of truth for Phase 2 (OS Build).*

---
---

# TEMPLATE: Pre-Deployment Audit Report

**Agent Name**: {{AGENT_NAME}}
**Audit Date**: {{DATE}}
**Auditor**: {{AUDITOR}}

### Results Summary

| Section | Status | Notes |
|---------|--------|-------|
| Proof of Action Protocol | {{STATUS_1}} | {{NOTES_1}} |
| Golden Dataset Accuracy | {{STATUS_2}} | {{NOTES_2}} |
| Security Guardrails | {{STATUS_3}} | {{NOTES_3}} |
| Cost and Loop Protection | {{STATUS_4}} | {{NOTES_4}} |
| Human Fallback | {{STATUS_5}} | {{NOTES_5}} |
| Post-Deployment Monitoring | {{STATUS_6}} | {{NOTES_6}} |

### Overall Verdict: {{VERDICT}}

### Failed Checks

{{FAILED_CHECKS_DETAIL}}

### Risk Acceptance (if applicable)

{{RISK_ACCEPTANCE}}

---

*Generated by Phase 3 (Pre-Deployment Audit).*

---
---

# TEMPLATE: OS Files

The following five templates are used in Phase 2 (OS Build) to generate the agent's operating system.

## SOUL.md Template

```markdown
# Soul

## Identity
{{AGENT_IDENTITY}}

## Tone
{{TONE_DESCRIPTION}}

## Boundaries
{{BEHAVIORAL_BOUNDARIES}}

## Values
{{VALUE_PRIORITIES}}
```

## AGENTS.md Template

```markdown
# Operating Manual

## Workflow: {{TASK_NAME}}

### Step 1: {{STEP_1_NAME}}
{{STEP_1_INSTRUCTIONS}}

### Step 2: {{STEP_2_NAME}}
{{STEP_2_INSTRUCTIONS}}

### Decision Point: {{DECISION_NAME}}
IF {{CONDITION}} THEN {{ACTION_A}}
ELSE {{ACTION_B}}

### Edge Case: {{EXCEPTION_NAME}}
WHEN {{TRIGGER}} THEN {{RESPONSE}}
```

## USER.md Template

```markdown
# User Profile

## Name: {{USER_NAME}}
## Role: {{ROLE}}

## Preferences
{{PREFERENCES}}

## Quality Standards
**Good Output**: {{GOOD_OUTPUT}}
**Bad Output**: {{BAD_OUTPUT}}
**Done Signal**: {{DONE_SIGNAL}}
```

## HEARTBEAT.md Template

```markdown
# Heartbeat

## Daily
- [ ] {{DAILY_TASK_1}}
- [ ] {{DAILY_TASK_2}}

## Weekly
- [ ] {{WEEKLY_TASK_1}}

## Monthly
- [ ] {{MONTHLY_TASK_1}}
```

## TOOLS.md Template

```markdown
# Authorized Tools

## {{TOOL_NAME}}
- **Purpose**: {{PURPOSE}}
- **Access Level**: {{ACCESS_LEVEL}}
- **Constraints**: {{CONSTRAINTS}}
```
