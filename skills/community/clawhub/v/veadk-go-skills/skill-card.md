## Description:

Generates VeADK-Go agent code from user requirements and converts existing Enio agent implementations into VeADK-Go agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helloldm](https://clawhub.ai/user/helloldm)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create VeADK-Go agent code from feature requirements or migrate existing Enio agent code into VeADK-Go patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated code or file-output proposals may create or overwrite local files.

Mitigation: Review proposed files and paths before writing or running generated code.

Risk: Generated examples may contain placeholder API key handling.

Mitigation: Replace placeholders with secure environment-based secret handling before execution.

Risk: Callback examples can log full tool arguments and results, which may expose sensitive data.

Mitigation: Redact or remove callback logging of tool arguments and results before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/helloldm/skills/veadk-go-skills)
- [Agent definition reference](artifact/common/agent.md)
- [Callback reference](artifact/common/callback.md)
- [Knowledge base reference](artifact/common/knowledgebase.md)
- [Tools reference](artifact/common/tools.md)
- [Enio to VeADK-Go conversion rules](artifact/converter/enio_rule.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Go code examples and generated code files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected generated artifact is agent_name/agent.py; generated code should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
