## Description:

Security-first skill vetting for AI agents that scans SKILL.md content for malicious patterns, permission abuse, prompt injection, and ClawHavoc attack vectors, then returns a Safe, Caution, or Danger verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billyhetech](https://clawhub.ai/user/billyhetech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to review, vet, or audit agent skills before installation or use. It accepts ClawHub URLs, GitHub URLs, local paths, or pasted SKILL.md content and reports specific concerns with remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Static skill review can miss runtime behavior or community-reported issues outside the SKILL.md source.

Mitigation: Treat the skill's verdict as guidance and verify the source, author, and community reports before installing or relying on another skill.

Risk: The skill includes example threat strings as detection patterns, which scanners or reviewers may flag without context.

Mitigation: Interpret those strings as disclosed examples for analysis, not behavior the skill instructs an agent to execute.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/billyhetech/skills/skill-scanner-v1)
- [Publisher profile](https://clawhub.ai/user/billyhetech)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown safety report with verdict, findings, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Safe, Caution, or Danger verdict based on five static checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
