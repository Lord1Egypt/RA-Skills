## Description:

Skill Safety Scanner audits installed ClawHub skills for dangerous code patterns and produces per-skill SAFE, WARN, or DANGEROUS reports with removal guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infectit007](https://clawhub.ai/user/infectit007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and ClawHub users use this skill to locally audit installed skills before trusting them, after installing new skills, or during incident response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review classifies the release as suspicious because its removal template includes an unsafe raw rm -rf command.

Mitigation: Prefer the official uninstall command or remove only a validated, canonical skill path after reviewing the exact command.

Risk: The scheduling example can persistently report scan findings to memory.

Mitigation: Enable scheduled reporting only after confirming where findings are stored and how untrusted evidence is sanitized.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/infectit007/skills/skill-safety-scanner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes SAFE/WARN/DANGEROUS ratings, evidence snippets, recommendations, and optional removal commands requiring confirmation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
