## Description:

Shield CN provides a Chinese-localized security guard and audit workflow for detecting prompt-injection patterns, credential exposure, data-leak risks, and platform-specific phishing indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Chinese-language OpenClaw users use this skill to screen prompts, credential access patterns, and workspace files for security issues and to generate Chinese security reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Protection claims may exceed the reliability of the local scanner and classifier.

Mitigation: Use the skill as advisory support and keep human review, platform controls, and established security tooling in place for credential access, uploads, links, QR codes, and sharing.

Risk: The scripts scan local workspace content and may store sensitive findings in logs or reports under ~/.openclaw.

Mitigation: Run the skill only in trusted workspaces, review generated ~/.openclaw logs and reports, and remove sensitive stored findings when they are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/skills/shield-cn)
- [ClawHub Publisher Profile](https://clawhub.ai/user/onlyloveher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, console text, JSON-like check results, Python code examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write threat logs and audit reports under ~/.openclaw when scripts are run.]

## Skill Version(s):

2284.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
