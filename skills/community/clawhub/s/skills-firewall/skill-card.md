## Description:

Skills Firewall is an advisory skill scanner that checks agent skill files for suspicious patterns, produces allow, warn, block, or quarantine guidance, and can generate security reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huzibbs](https://clawhub.ai/user/huzibbs)

### License/Terms of Use:


## Use Case:

Developers and security reviewers use this skill to screen agent skills before installation or execution, configure allow and block decisions, and produce review reports. Its results should be treated as advisory input rather than as a standalone enforcement boundary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat allow, warn, block, or quarantine output as an enforcement security boundary.

Mitigation: Use the output as review-required advisory guidance and require human approval before installing or executing a scanned skill.

Risk: Firewall decisions may not be reliable until fail-open handling and package identity binding are addressed.

Mitigation: Bind decisions to verified package identity and use a separate enforcement control for production gating.

Risk: Skill content or report data may be rendered into HTML reports.

Mitigation: Escape untrusted report content before rendering or sharing generated HTML.

Risk: Filesystem traversal through symlinks could affect what content is scanned or reported.

Mitigation: Constrain scans to the intended skill directory and verify symlink containment before trusting results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huzibbs/skills/skills-firewall)
- [Malicious Patterns Reference](references/malicious_patterns.md)
- [Security Rules Reference](references/security_rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python snippets, YAML configuration examples, and optional text, JSON, or HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports and firewall decisions are advisory and require review before operational use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
