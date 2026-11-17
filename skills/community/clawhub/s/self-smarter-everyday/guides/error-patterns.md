# Error Pattern Recognition Guide

## Overview

Every error the agent encounters is a learning opportunity. The Self-Smarter-Everyday skill includes a systematic error pattern recognition system that categorizes errors, identifies root causes, detects recurring patterns, suggests automatic fixes, and builds a growing library of error knowledge. Over time, this system transforms the agent from something that makes the same mistake twice into something that anticipates and prevents errors before they occur.

This guide covers the complete error pattern lifecycle: from detection to prevention.

---

## Common Error Types

### Category 1: Tool Execution Errors

These occur when a tool call fails or produces unexpected results.

**Subtypes:**

- **Command not found** — A CLI tool or binary is missing from the environment.
- **Permission denied** — The agent lacks permissions to perform the requested operation.
- **Timeout** — A tool call exceeded its time limit (network request, SSH command, API call).
- **Exit code non-zero** — A command executed but returned an error status.
- **Parse failure** — Tool output couldn't be parsed (malformed JSON, unexpected format).
- **Resource exhausted** — Out of memory, disk full, or rate limit exceeded.

**Example:**
```
Error: SSH command timed out after 30s
Command: docker compose up -d --build
Root cause: Container build triggered a full dependency reinstall
Fix: Increase timeout or pre-cache dependencies
```

### Category 2: Logic Errors

These occur when the agent's reasoning leads to an incorrect conclusion or action.

**Subtypes:**

- **Wrong assumption** — The agent assumed something that turned out to be false.
- **Missing context** — The agent didn't consider relevant information.
- **Over-generalization** — A rule was applied too broadly.
- **Off-by-one** — Boundary conditions were handled incorrectly.
- **Race condition** — The agent didn't account for timing dependencies.

**Example:**
```
Error: Agent reported "website accessible" but it was actually a 404 page
Root cause: curl returned HTTP 200 for Vercel's custom 404 page
Fix: Always verify with browser screenshot, not just HTTP status
```

### Category 3: Communication Errors

These occur when the agent's output doesn't match what the user expected.

**Subtypes:**

- **Misunderstood intent** — The agent solved a different problem than the user intended.
- **Wrong format** — The output format didn't match expectations (markdown table in WhatsApp, code block when prose was needed).
- **Tone mismatch** — The response tone was inappropriate for the context.
- **Information leak** — Internal system details were exposed to the user.
- **Incomplete response** — The response addressed part of the request but missed other parts.

### Category 4: Integration Errors

These occur when external systems behave unexpectedly.

**Subtypes:**

- **API changes** — An external API changed its response format or endpoints.
- **Authentication failure** — Tokens expired, credentials changed, or OAuth flows broke.
- **Service downtime** — An external service was temporarily unavailable.
- **Rate limiting** — The agent hit rate limits on external APIs.
- **Data format mismatch** — Data from one system couldn't be consumed by another.

### Category 5: Resource Errors

These occur when the agent's environment has insufficient resources.

**Subtypes:**

- **Memory exhaustion** — OOM killer terminated a process.
- **Disk full** — No space left for writes.
- **Context window overflow** — Too much information in the prompt.
- **Token budget exceeded** — Daily spending limit reached.
- **Concurrency limit** — Too many simultaneous operations.

---

## Pattern Detection

### How Patterns Are Detected

The nightly routine analyzes all errors from the past 24 hours and looks for patterns using several techniques:

**1. Frequency Analysis**

Count how often each error type occurs. Errors that appear 3+ times in a single day or 5+ times in a week are flagged as patterns.

**2. Similarity Clustering**

Group errors by semantic similarity. Two errors that look different on the surface may share the same root cause. For example:

- "SSH connection refused" and "docker container not running" may both stem from the same service being down.
- "JSON parse error" and "unexpected token" may both stem from an API returning HTML instead of JSON.

**3. Temporal Correlation**

Check if errors cluster in time. A burst of errors around a specific time may indicate:

- A deployment that broke something
- An external service outage
- A configuration change that had unintended effects
- A resource exhaustion event (end-of-day disk full, memory leak)

**4. Causal Chain Detection**

Trace error sequences to find root causes. When Error A consistently leads to Error B which leads to Error C, fixing A prevents the entire chain.

### Pattern Detection Algorithm

```
For each error in today's error log:
  1. Extract error signature (type, tool, command, error message)
  2. Compare against known patterns in the error pattern library
  3. If match found → increment pattern frequency counter
  4. If no match → create new candidate pattern
  5. Check for causal chains with preceding errors
  6. Update pattern metadata (first seen, last seen, frequency, contexts)
```

---

## Categorization

### Error Severity Levels

| Level | Name | Definition | Response |
|-------|------|------------|----------|
| 1 | **Critical** | Agent cannot function. Task completely failed. User impacted. | Immediate fix required. Flag in nightly report. |
| 2 | **High** | Task failed but workaround exists. User mildly impacted. | Fix within 24 hours. Suggest workaround. |
| 3 | **Medium** | Task completed with degraded quality. User may not notice. | Fix within 72 hours. Log for tracking. |
| 4 | **Low** | Minor issue. No user impact. Cosmetic or efficiency concern. | Fix when convenient. Track trend. |
| 5 | **Info** | Not really an error. Unexpected but acceptable outcome. | Log for awareness. No action needed. |

### Error Taxonomy

Each error is tagged with a structured taxonomy:

```json
{
  "id": "err-2026-08-10-042",
  "timestamp": "2026-08-10T14:23:00+07:00",
  "category": "tool-execution",
  "subcategory": "timeout",
  "severity": 2,
  "tool": "exec",
  "command": "docker compose up -d --build",
  "errorMessage": "Command timed out after 30s",
  "context": "Deploying client application to VPS",
  "rootCause": "Container build triggered full dependency reinstall",
  "patternMatch": "pattern-build-timeout-001",
  "resolution": "Increased timeout to 120s and added dependency caching",
  "preventedByFuture": "pre-2026-08-11-001"
}
```

---

## Root Cause Analysis

### The 5 Whys Method

For each significant error pattern, the nightly routine performs a structured root cause analysis using the "5 Whys" technique:

**Example:**

Error: Agent sent internal system output to user via WhatsApp.

1. **Why?** — The agent echoed sub-agent completion output directly.
2. **Why?** — The agent didn't distinguish between internal evidence and user-facing response.
3. **Why?** — The prompt didn't explicitly instruct to rewrite sub-agent output.
4. **Why?** — This failure mode wasn't anticipated when the prompt was written.
5. **Why?** — The sub-agent architecture was added after the original prompt design.

**Root cause:** Prompt needs explicit instruction about sub-agent output handling.

**Fix:** Add rule to AGENTS.md: "Sub-agent completion event = BUKAN pesan WhatsApp. Rewrite in your own voice."

### Root Cause Categories

After analysis, each root cause is categorized:

- **Prompt gap** — The instructions don't cover this scenario.
- **Knowledge gap** — The agent lacks information needed for this task.
- **Tool limitation** — The available tools can't handle this case.
- **Environment issue** — The runtime environment has a problem.
- **Design flaw** — The overall approach or architecture is wrong.
- **External dependency** — An external system changed or failed.

---

## Automatic Fix Suggestions

### How Fix Suggestions Work

When a pattern is identified and root-caused, the system generates fix suggestions:

**For prompt gaps:**
- Generate a specific prompt mutation that addresses the gap.
- Submit to the prompt evolution phase for testing and potential application.

**For knowledge gaps:**
- Identify what information is missing.
- Suggest creating a memory entry or reference document.
- If the knowledge is externally available, suggest a web search or documentation review.

**For tool limitations:**
- Suggest alternative tools or workarounds.
- If no alternative exists, flag for human review.
- Consider creating a skill that wraps the limitation with error handling.

**For environment issues:**
- Generate a diagnostic script to identify the specific problem.
- Suggest configuration changes.
- Flag for human review if infrastructure access is needed.

### Fix Confidence Scoring

Each fix suggestion receives a confidence score:

| Confidence | Meaning | Action |
|------------|---------|--------|
| 0.8-1.0 | High confidence this fix addresses the root cause | Apply automatically (if safe) |
| 0.5-0.79 | Moderate confidence | Include in nightly report for human review |
| 0.2-0.49 | Low confidence | Log for tracking, don't apply |
| 0.0-0.19 | Speculative | Discard, need more data |

---

## Learning from Errors

### The Error Learning Loop

```
Error occurs
  → Logged with full context
  → Nightly routine analyzes
  → Pattern detected (if recurring)
  → Root cause identified
  → Fix suggested
  → Fix applied (if safe and confident)
  → Next occurrence monitored
  → If error doesn't recur → fix validated
  → If error recurs → fix was insufficient, try again
```

### Error-to-Lesson Conversion

Significant errors are converted into lessons and stored in the `lessons/` directory:

```markdown
## Lesson: Always verify web pages with browser, not just curl

**Date:** 2026-08-10
**Severity:** High
**Category:** Tool Selection

### What happened:
Agent reported "website accessible" based on curl returning HTTP 200.
User visited the URL and got a 404 page.

### Root cause:
Vercel returns HTTP 200 for custom 404 pages. curl only checks HTTP status,
not page content. Browser rendering reveals the actual page state.

### Fix applied:
Added rule to AGENTS.md: "WAJIB test dari sisi aku dulu sebelum bilang selesai.
Use browser tool for web pages, curl only for API endpoints."

### Prevention:
- Always use browser screenshot for web page verification
- curl is only for API healthchecks
- Never trust HTTP status alone for JS-rendered pages
```

---

## Building an Error Pattern Library

### Library Structure

```
data/error-patterns/
├── library.json              # Index of all known patterns
├── patterns/
│   ├── tool-execution/
│   │   ├── timeout-build.json
│   │   ├── permission-denied-docker.json
│   │   └── ...
│   ├── logic/
│   │   ├── wrong-assumption-repo-exists.json
│   │   └── ...
│   ├── communication/
│   │   ├── subagent-output-leak.json
│   │   └── ...
│   ├── integration/
│   │   ├── api-format-change.json
│   │   └── ...
│   └── resource/
│       ├── oom-killer.json
│       └── ...
└── resolved/
    └── ... # Patterns that haven't recurred in 30+ days
```

### Pattern Entry Format

```json
{
  "id": "pattern-timeout-build-001",
  "category": "tool-execution",
  "subcategory": "timeout",
  "signature": {
    "tool": "exec",
    "commandPattern": "docker compose up.*--build",
    "errorPattern": "timed out after \\d+s"
  },
  "rootCause": "Container build triggers full dependency reinstall",
  "firstSeen": "2026-07-19",
  "lastSeen": "2026-08-10",
  "occurrences": 7,
  "severity": 2,
  "fixes": [
    {
      "description": "Increase exec timeout to 120s for build commands",
      "confidence": 0.85,
      "applied": true,
      "effective": true
    },
    {
      "description": "Add dependency caching layer to Dockerfile",
      "confidence": 0.70,
      "applied": false,
      "effective": null
    }
  ],
  "status": "active"
}
```

---

## Prevention Strategies

### Strategy 1: Pre-Flight Checks

Before executing high-risk operations, run pre-flight checks based on known error patterns:

- Before SSH operations → check `free -m` and `df -h` (prevents OOM)
- Before web deployment → check container status and DNS (prevents 404 incidents)
- Before sending messages → verify content doesn't contain internal data (prevents leaks)

### Strategy 2: Error-Aware Prompting

Incorporate known error patterns directly into the agent's prompts:

```markdown
## Known Pitfalls (from error pattern library)
- curl HTTP 200 ≠ page is correct. Always browser-verify web pages.
- Sub-agent output is internal evidence, not user-facing text. Always rewrite.
- Check `free -m` before heavy SSH operations to prevent OOM.
- Never self-update container from inside the container.
```

### Strategy 3: Guard Rails

Implement automatic guard rails for high-risk operations:

- **Timeout guard:** If a command has timed out before, automatically use a longer timeout.
- **Permission guard:** If an operation has failed with permission errors before, check permissions first.
- **Format guard:** If an API has returned unexpected formats before, add response validation.

### Strategy 4: Progressive Disclosure

Start with safe operations and escalate gradually:

- Test with dry-run before real execution
- Test with small data before large batches
- Test in sandbox before production

---

## Summary

Error pattern recognition transforms failures into fuel for improvement. By systematically categorizing errors, detecting patterns, analyzing root causes, suggesting fixes, and building a growing library of error knowledge, the agent becomes progressively more resilient. The goal is not to eliminate all errors — that's impossible — but to ensure the same error never happens twice, and that known error patterns are anticipated and prevented before they cause harm. Over time, the error pattern library becomes one of the agent's most valuable assets, encoding hard-won operational knowledge that would otherwise be lost.
