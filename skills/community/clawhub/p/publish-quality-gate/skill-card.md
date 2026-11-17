## Description:

Reviews skills, documents, tools, and other release materials for sensitive information before publication and for quality across five TRACE dimensions afterward.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release maintainers use it to review a specified skill, document, tool, or expert pack before external distribution and to perform a TRACE self-assessment after publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release checker may approve content containing secrets and may expose files outside the selected folder.

Mitigation: Review releases independently for secrets; use an isolated copy without symlinks, treat reports as sensitive, and require containment checks, output redaction, corrected exemptions, and input validation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/zhaoxinghua09-cell/skills/publish-quality-gate)
- [Project homepage](https://zhaoxinghua09-cell.github.io/lgd-hub/)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Text quality report with per-layer findings and a TRACE assessment when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes review findings and a pass, warning, or failure status.]

## Skill Version(s):

1.0.12 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
