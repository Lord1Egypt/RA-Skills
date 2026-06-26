# STRIDE Threat Model

**Platforms:** Claude · Openclaw · Codex
**Domain:** Cybersecurity

## Purpose

Turns a system or feature architecture description into a STRIDE-categorized threat model: an asset list, trust-boundary map, per-threat risk scoring, and recommended mitigations grouped by control type. Designed to run during design review, security-architecture review, or as part of a pre-launch threat-modeling session.

## When to Use

- Security engineer or architect running a threat-modeling session for a new feature
- Application-security reviewer assessing a design doc before sign-off
- DevSecOps lead integrating STRIDE review into a CI/CD design-review gate
- Engineering manager threat-modeling a service before its first production deploy
- Product security team reviewing a third-party integration or new data flow

## What It Does

**Phase 1: Scoping**
1. Captures the system under analysis: components, data flows, trust boundaries, assets, user roles, deployment topology, and tech stack
2. Confirms the review scope and any out-of-scope components

**Phase 2: Decomposition & Threat Discovery**
3. Builds an asset list and a text-based trust-boundary map (entries, exits, crossings)
4. Walks each component × data flow against the six STRIDE categories (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege) and logs every plausible threat with evidence anchored to the design

**Phase 3: Risk & Mitigation**
5. Scores each threat (Likelihood × Impact) into a Risk tier with a written justification
6. Recommends mitigations grouped by control type (AuthN/AuthZ, Crypto, Logging/Monitoring, Input/Output, Network/Isolation, Operational)
7. Produces the Top-N threats list, an open-questions list for the design author, and the audit-ready STRIDE report

## Output

A structured STRIDE report with asset list, trust-boundary map, per-threat table (STRIDE category, component, attack scenario, evidence, likelihood, impact, risk, mitigation, status), Top-N prioritized threats, mitigation backlog grouped by control type, and an unresolved-information list. Ready to attach to a design doc or security-review ticket.

## Safety Notes

The skill never executes attacks, never scans systems, and never produces working exploit code. Mitigation recommendations are advisory — engineering owners and security reviewers must implement and validate. The skill treats component names, hostnames, IPs, and secrets disclosed in the session as confidential and never reuses them in examples. If the framing suggests offensive use against a system the user does not own or operate, the skill asks for the defensive context before continuing.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.