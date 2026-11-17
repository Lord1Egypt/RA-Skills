## Description:

Implements a three-layer self-improvement process for agents to evaluate task outcomes, record lessons, generate optimization plans, and share learning across agent workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandon114](https://clawhub.ai/user/brandon114)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to evaluate agent task performance, capture lessons, create optimization plans, and share reviewed learning across WorkBuddy agent workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evaluation records and lessons can retain sensitive task details in local JSON files.

Mitigation: Avoid recording secrets, customer data, private prompts, or unreviewed instructions, and review records before retaining them.

Risk: Shared lessons can be copied to other local WorkBuddy agent workspaces without granular scoping.

Mitigation: Run the sync step only after reviewing collective-wisdom.json and confirming the intended target workspaces.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/brandon114/skills/self-improving-agent-python)
- [English README](artifact/README_en.md)
- [English skill instructions](artifact/SKILL_en.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON records written by helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists evaluations, lessons, optimization plans, and shared knowledge under local WorkBuddy workspace directories.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact SKILL files state 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
