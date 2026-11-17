## Description:

Security vetting protocol before installing any AI agent skill, with red flag detection for credential theft, obfuscated code, exfiltration, structured risk classification, and vetting reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[firebroo](https://clawhub.ai/user/firebroo)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to review AI agent skills before installation, identify security red flags, classify risk, and produce an installation recommendation. It is intended for ClawHub, GitHub, and other externally sourced skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ClawHub vetting workflow instructs agents to install untrusted skills into a temporary directory before completing review.

Mitigation: Use a download-only or sandboxed inspection method before any clawhub install operation is run on an untrusted skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/firebroo/skills/security-skiil-scanner)
- [Publisher Profile](https://clawhub.ai/user/firebroo)
- [Skill Homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports, checklists, risk classifications, recommendations, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces LOW, MEDIUM, HIGH, or EXTREME risk classifications with install recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
