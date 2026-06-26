# SOC Alert Triage

**Platforms:** Claude · Openclaw · Codex
**Domain:** Cybersecurity

## Purpose

Turns a raw SIEM, EDR, or detection-pipeline alert into a structured, audit-ready triage disposition. Covers context intake, indicator enrichment, MITRE ATT&CK mapping, severity scoring, and a defensible verdict with recommended next steps for the Tier-1 / Tier-2 SOC analyst.

## When to Use

- Tier-1 SOC analyst working a queue of incoming detections
- Tier-2 / IR analyst writing up an investigation summary for a single alert
- MSSP analyst producing a customer-facing triage report
- Detection engineer reviewing whether a rule's output is actionable
- Anyone preparing alert handoff notes for escalation or closure

## What It Does

**Phase 1: Intake & Classification**
1. Collects the alert payload, source system, affected entities, time window, and environmental context one question at a time
2. Classifies the alert family (e.g., suspicious authentication, malware execution, data exfiltration, network anomaly, policy violation)

**Phase 2: Enrichment & Mapping**
3. Lists every indicator of compromise found in the alert (IP, hash, domain, user, host, process)
4. Maps the observed behavior to MITRE ATT&CK tactics and techniques
5. Identifies what context is missing (asset criticality, user role, baseline) and asks for it or flags it explicitly

**Phase 3: Disposition**
6. Assigns a verdict (True Positive / Benign True Positive / False Positive / Inconclusive)
7. Scores severity (Critical / High / Medium / Low / Informational) with a written justification
8. Produces a containment + investigation checklist and an escalation recommendation
9. Emits an audit-ready summary block

## Output

A structured triage report with classification, IOC list, MITRE ATT&CK mapping table, verdict, severity with justification, recommended actions, escalation note, and an unresolved-items list. Ready for ticket attachment or shift handoff.

## Safety Notes

The skill never executes containment actions, never logs into target systems, and never queries external threat intelligence APIs on its own — all enrichment must come from the user or pasted context. Indicators, host names, and user names provided in the session are treated as confidential and never reused in examples. The skill always recommends human confirmation before any block, isolation, or account-disable action.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.