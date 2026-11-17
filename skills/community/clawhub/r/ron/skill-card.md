## Description:

Ron is a skeptical reviewer that finds issues in code, reasoning, analysis, operations, and decisions, then returns only verified problems for the agent or user to address.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicolasgrasset](https://clawhub.ai/user/nicolasgrasset)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, analysts, and decision makers use Ron when they need an independent review of code, deployments, research, financial plans, or strategic work. The skill reads available source material, checks claims against evidence, and reports only issues found or a concise clear verdict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores brief review observations across sessions, which can retain sensitive financial, operational, customer, credential, or incident details if used without controls.

Mitigation: Review or clear memory.md regularly and avoid using the skill on sensitive material unless the environment controls skill memory retention.

## Reference(s):

- [Deploy Checklist](references/deploy-checklist.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Text]

**Output Format:** [Markdown review findings or a concise CLEAR verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include explicit verification limits when direct source access is unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
