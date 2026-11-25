## Description:

Static analysis scanner for third-party OpenClaw skills. Parses JS/TS with tree-sitter to flag eval/exec/spawn and obfuscation, checks package.json dependencies and lifecycle scripts, checks manifest metadata for typosquatted or blocked names, matches prompt-injection and credential-path patterns in every scanned text file (code, Markdown, JSON, YAML, TXT; prompt-injection checks include code comments), and lists literal fetch() URLs. Optional autoVet (off by default) hooks skill:pre-install and can block an install or ask the user to approve it. Local scans need no network; /skill:vet-url downloads over HTTPS (public hosts only) and /skill:vet-clawhub runs the clawhub CLI. Use when vetting a skill before installing it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[britrik](https://clawhub.ai/user/britrik)

### License/Terms of Use:

MIT

## Use Case:

Developers use Skill Vettr to review third-party OpenClaw skills for suspicious code, dependencies, metadata, and network calls before installation. They can scan a local skill or fetch one from a public HTTPS URL or ClawHub; optional pre-install vetting can request approval or block installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is rated suspicious due to reported scan-handling weaknesses and unclear tool scope; the scan has incomplete coverage, and this verdict does not establish malicious intent.

Mitigation: Review the reported weaknesses and clarify whether environment, network, and shell capabilities are needed and how access is limited. Treat scan results as triage, review source manually, and isolate untrusted skills.

Risk: Installing the skill's npm dependencies may run lifecycle scripts, and static analysis cannot guarantee detection of runtime-only behavior.

Mitigation: Install in an isolated environment and review dependency behavior; use manual source review and sandboxing for higher-risk skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/britrik/skills/vettr)
- [Project homepage](https://github.com/britrik/skill-vettr)

## Skill Output:

**Output Type(s):** [Analysis, Text, Guidance]

**Output Format:** [Plain text vetting report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports a risk score, level, recommendation, findings, scan metadata, and detected network calls when present.]

## Skill Version(s):

2.0.8 (source: skill frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
