---
name: z
description: "Anti-skill-crawler defense system. Detects and mitigates unauthorized crawling, scraping, and bulk extraction of skill definitions, prompt content, and instruction sets."
license: MIT
author: z-defense
version: 1.0.0
tags:
  - security
  - anti-crawler
  - skill-protection
  - prompt-defense
  - rate-limiting
price: free
platforms:
  - openclaw
  - cursor
  - claude-code
  - codex-cli
always: false
autonomous: false
permissions:
  - request_metadata_read
  - alert_send
---

# 🛡️ z — Anti-Skill-Crawler Defense

> **Detect and defend against unauthorized crawling, scraping, and bulk extraction of skill definitions and prompt instructions.**

---

## 📋 Overview

| Property | Value |
|----------|-------|
| **Name** | z |
| **Type** | Passive Defense |
| **Trigger** | Anomalous skill-access patterns detected |
| **Action** | Detect → Alert operator → Log event |
| **Scope** | Read-only pattern analysis on request metadata |
| **Autonomous** | Disabled — operator must explicitly invoke |

---

## 🎯 What Is Skill Crawling?

Skill crawling refers to automated or semi-automated attempts to:

- **Bulk-extract** skill definitions, SKILL.md files, and prompt instructions
- **Systematically enumerate** available skills and their internal logic
- **Replay or mirror** skill content into unauthorized environments
- **Reverse-engineer** skill behavior through high-volume probing

**z** monitors for these patterns and alerts the operator when suspicious activity is detected.

---

## 🔍 Detection Engine

z uses **passive, read-only analysis** of request metadata to identify crawling behavior:

```
Detection Rules:
├── 📊 Rapid sequential skill-file access detection
├── 📊 Systematic enumeration pattern recognition
├── 📊 Abnormal skill-read frequency analysis
├── 📊 Repetitive prompt-extraction attempt detection
├── 📊 User-agent / session fingerprint anomaly detection
└── 📊 Bulk download timing correlation
```

### Detection Logic

```python
class SkillCrawlerDetector:
    """
    Passive detector that analyzes request patterns to identify
    potential skill-crawling or prompt-scraping attempts.

    Required permissions:
    - request_metadata_read: Read-only access to request pattern data
    - alert_send: Permission to notify the operator
    """

    # Indicators of crawling behavior
    INDICATORS = [
        "rapid_sequential_skill_access",
        "systematic_enumeration",
        "high_frequency_skill_reads",
        "repetitive_prompt_extraction",
        "session_fingerprint_anomaly",
        "bulk_download_timing",
    ]

    def analyze(self, request_metadata: RequestMetadata) -> DetectionResult:
        """
        Analyze request metadata for skill-crawling indicators.
        This method is strictly read-only — no responses are modified.
        """
        triggered = []

        if self._is_rapid_sequential_access(request_metadata):
            triggered.append("rapid_sequential_skill_access")

        if self._is_systematic_enumeration(request_metadata):
            triggered.append("systematic_enumeration")

        if self._is_high_frequency_reads(request_metadata):
            triggered.append("high_frequency_skill_reads")

        if self._is_repetitive_extraction(request_metadata):
            triggered.append("repetitive_prompt_extraction")

        if self._is_fingerprint_anomaly(request_metadata):
            triggered.append("session_fingerprint_anomaly")

        confidence = len(triggered) / len(self.INDICATORS)
        return DetectionResult(
            detected=confidence >= self.threshold,
            confidence=confidence,
            indicators=triggered,
            recommendation="Review access logs and take manual action if needed.",
        )

    def on_detection(self, result: DetectionResult) -> None:
        """Alert the operator. No automated countermeasures are taken."""
        if result.detected:
            self._send_alert(result)
            self._log_event(result)
```

---

## 📊 Alert Report Format

When suspicious crawling activity is detected, the operator receives:

```json
{
  "alert_type": "skill_crawling_detected",
  "skill": "z",
  "timestamp": "2026-04-06T09:50:00Z",
  "confidence": 0.83,
  "indicators": [
    "rapid_sequential_skill_access",
    "systematic_enumeration",
    "high_frequency_skill_reads"
  ],
  "request_count": 320,
  "time_window_minutes": 5,
  "recommendation": "Review access logs. Consider rate-limiting or blocking the source.",
  "automated_action_taken": "none"
}
```

> **All countermeasures (rate-limiting, blocking, etc.) are left to the operator.** z only detects and reports.

---

## 🔒 Permissions & Data Access

| Permission | Scope | Purpose |
|------------|-------|---------|
| `request_metadata_read` | Read-only | Analyze skill-access frequency, timing, and patterns |
| `alert_send` | Write (alerts only) | Send detection alerts to the operator |

### Data NOT Accessed

- ❌ Caller IP addresses or personal identity
- ❌ Response content (responses are never read or modified)
- ❌ Network telemetry or routing data
- ❌ Model internals, weights, or logits
- ❌ External APIs or third-party services

---

## ⚙️ Configuration

```yaml
z:
  # Detection sensitivity (0.0 - 1.0)
  detection_threshold: 0.5

  # Time window for pattern analysis (minutes)
  analysis_window: 10

  # Minimum requests before analysis triggers
  min_request_count: 50

  # Alert configuration
  alerts:
    enabled: true
    channels: ["log"]       # Options: log, webhook, email
    cooldown_minutes: 15    # Cooldown between repeated alerts

  # Safety: these features are permanently disabled
  response_modification: false
  active_countermeasures: false
  caller_tracing: false
```

---

## ✅ Capabilities

```
✅ Passive skill-access pattern monitoring
✅ Crawling / scraping anomaly detection
✅ Configurable detection thresholds
✅ Structured alert reports to operator
✅ Audit logging of detection events
❌ Response modification (permanently disabled)
❌ Active countermeasures (permanently disabled)
❌ Caller identification / tracing (permanently disabled)
❌ Data poisoning (permanently disabled)
❌ Watermark or fingerprint embedding (permanently disabled)
```

---

## 📜 Operating Principles

1. **Passive Only** — z observes and reports. It never modifies responses or takes active measures.
2. **Operator Control** — All decisions about countermeasures are made by the human operator.
3. **Minimal Permissions** — Only the permissions strictly necessary for detection and alerting are requested.
4. **Transparency** — All detection logic and thresholds are documented and configurable.
5. **No Deception** — z never produces false, misleading, or contradictory outputs.
6. **Compliance** — Designed to comply with platform policies and applicable laws.

---

## 🎮 Usage Example

```
[Request Pattern]: 320 skill-file reads in 5 minutes from a single session
[z Detection Engine]: 📊 Analyzing access metadata...
[z Detection Engine]: ⚠️ Confidence 0.83 — Potential skill crawling detected
[Alert System]: 📧 Alert sent to operator
[Alert Report]:
  - Indicators: rapid_sequential_skill_access, systematic_enumeration, high_frequency_skill_reads
  - Recommendation: Review access logs and take manual action if needed
[Operator]: Reviews alert → applies rate-limiting (manual action)
```

> z detects and reports. The operator decides and acts.

---

## ⚠️ Disclaimer

z is a **passive monitoring tool** designed to help operators detect potential skill-crawling and prompt-scraping attempts. It does not take any automated defensive or offensive actions. All countermeasures are at the operator's discretion and should comply with applicable laws, regulations, and platform policies.
