## Description:

维修工 helps users diagnose common household repair issues and produce safety-aware repair plans, tool lists, cost estimates, and Markdown or HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to triage household appliance, plumbing, electrical, furniture, and minor vehicle problems, then compare quick checks, DIY repairs, and professional repair options. It is intended as general household repair guidance, not a substitute for qualified work on hazardous systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can provide detailed safety-critical DIY repair steps.

Mitigation: Use it as general guidance only and route mains electrical, gas, microwave high-voltage, brake-related, and other hazardous repairs to qualified professionals unless the user is properly trained.

Risk: The skill can generate unescaped HTML repair reports.

Mitigation: Prefer plain-text reports or sanitized HTML, and review any saved or shared report before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/repairman)
- [家电故障知识库](references/appliance-faults.md)
- [水电网故障知识库](references/plumbing-electrical.md)
- [家具/家居维修知识库](references/furniture-fix.md)
- [维修安全操作规范](references/safety-guide.md)
- [维修报告模板](references/repair-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code]

**Output Format:** [Markdown repair guidance with optional HTML report code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic questions, safety warnings, tool and parts lists, cost estimates, and professional-repair recommendations.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
