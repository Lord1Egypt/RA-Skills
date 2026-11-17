## Description:

Routing Optimization helps agents analyze dispatch logs, compare routing strategies, and propose routing-rule adjustments to improve hit rate, accuracy, and dispatch performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to evaluate routing-rule performance from dispatch logs, run A/B comparisons, and prepare routing optimization recommendations before changing live rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dispatch logs used for routing analysis may contain prompts, user identifiers, business data, or secrets.

Mitigation: Use minimized or redacted logs and confirm the log source before applying the skill.

Risk: Routing-rule recommendations may reduce accuracy or route work to the wrong agent if applied automatically.

Mitigation: Review generated rule changes manually and test them before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daxiangnaoyang/skills/routing-optimization)
- [Publisher Profile](https://clawhub.ai/user/daxiangnaoyang)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Python, PowerShell, JSON, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include routing metrics, A/B test comparisons, optimization suggestions, and configuration examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
