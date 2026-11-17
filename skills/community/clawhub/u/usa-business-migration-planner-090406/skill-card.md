## Description:

Helps users plan non-Cloudflare CDN options for workloads constrained by Cloudflare's 120-second timeout and an approximately ¥1000 monthly budget.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn CDN vendor-selection requests into a practical migration plan, checklist, analysis, code, shell commands, configuration, or decision support for non-Cloudflare options under stated budget and timeout constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill label does not match its actual CDN-selection content, which may mislead users about the intended business migration scope.

Mitigation: Review the name and presented purpose before deployment; use it for CDN or vendor-selection tasks unless it is renamed and rescoped.

Risk: Broad activation metadata may cause the skill to run for unrelated general-help or V2EX requests.

Mitigation: Scope invocation to explicit CDN, Cloudflare timeout, bandwidth, or migration-planning requests.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/usa-business-migration-planner-090406)
- [V2EX CDN Requirement](https://www.v2ex.com/t/1229340)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, checklists, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, validation notes, remaining risks, and next-step guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
