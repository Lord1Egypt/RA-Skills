## Description: <br>
Define, manage, and compile business rules as structured YAML data into LLM-ready prompts and agent-loadable SKILL.md files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pallaoro](https://clawhub.ai/user/pallaoro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations teams, and policy owners use Rule Spec to author and maintain business rules in rulespec.yaml, validate them, and emit agent-loadable SKILL.md guidance without manually editing generated skill files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SKILL.md files may contain incorrect or stale business-rule guidance if accepted without review. <br>
Mitigation: Review generated SKILL.md files before loading them into an agent and run rulespec validate after direct rulespec.yaml edits. <br>
Risk: Rule examples can contain sensitive operational or customer data. <br>
Mitigation: Avoid putting sensitive examples into rule files unless necessary, and confirm examples are safe before emitting or sharing generated skills. <br>
Risk: The workflow uses the external rulespec npm package through npx commands. <br>
Mitigation: Verify the rulespec npm package before running npx commands in trusted environments. <br>


## Reference(s): <br>
- [Rule Spec on ClawHub](https://clawhub.ai/pallaoro/rulespec) <br>
- [Clawnify](https://www.clawnify.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with YAML, TypeScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of the rulespec CLI to manage rulespec.yaml and emit SKILL.md files; examples are excluded from emitted SKILL.md by default.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
