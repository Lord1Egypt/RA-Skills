## Description: <br>
Skill Composer orchestrates multiple OpenClaw skills into YAML-defined workflows that can be previewed, validated, and run from a CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to define multi-step OpenClaw workflows in YAML, pass outputs between steps, preview workflow execution, validate workflow syntax, and run installed skills in sequence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow manifests can invoke any installed skill, which gives a workflow broad authority over local files, credentials, publishing steps, and external service calls. <br>
Mitigation: Run only trusted workflow manifests, review each step before execution, and require explicit confirmation before workflows write files, use credentials, publish content, or call external services. <br>
Risk: The security evidence flags unsafe condition evaluation in workflow logic. <br>
Mitigation: Avoid untrusted condition expressions and review the condition-handling code before installing or running workflows from outside trusted sources. <br>
Risk: The install script may install PyYAML through system or user package managers. <br>
Mitigation: Install in a controlled environment and review dependency installation commands before running the installer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utopiabenben/skill-composer) <br>
- [Project homepage](https://github.com/utopiabenben/ai-skills) <br>
- [Publisher profile](https://clawhub.ai/user/utopiabenben) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text output and YAML workflow configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Workflows can pass file path references between sequential steps and may produce additional files through the invoked skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
