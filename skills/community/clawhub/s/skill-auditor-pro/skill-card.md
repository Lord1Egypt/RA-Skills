## Description:

Security scanner for ClawHub skills. Detects malicious code, obfuscated payloads, and social engineering before installation. Three-layer analysis: pattern matching, deobfuscation, and LLM intent analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sypsyp97](https://clawhub.ai/user/sypsyp97)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to inspect ClawHub skills before installation and flag suspicious patterns, obfuscated payloads, social engineering indicators, and risky execution behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write extracted suspicious code to a predictable shared temporary path.

Mitigation: Run it as an unprivileged user in a disposable or single-user environment, and avoid scanning directories that contain private source or secrets until the temporary-file behavior is fixed.

Risk: The documentation overstates LLM analysis behavior compared with the artifact's handoff-style implementation.

Mitigation: Treat the LLM step as reviewer guidance rather than automatic semantic analysis unless the implementation and documentation are corrected.

## Reference(s):

- [Skill Auditor Pro ClawHub listing](https://clawhub.ai/sypsyp97/skills/skill-auditor-pro)
- [341 Malicious ClawHub Skills Incident](https://thehackernews.com/2026/02/researchers-find-341-malicious-clawhub.html)
- [OpenClaw Security Guide](https://docs.openclaw.ai/gateway/security)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text report with risk findings, line references, suspicious code preview, and verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a nonzero shell exit code when medium or high risk findings are detected.]

## Skill Version(s):

2.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
