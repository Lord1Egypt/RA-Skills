## Description: <br>
Guide for creating effective skills. This skill should be used when users want to create a new skill or update an existing skill that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangkang5](https://clawhub.ai/user/wangkang5) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and skill authors use this skill to design, initialize, validate, package, and iterate on agent skills with concise instructions, reusable scripts, references, and assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or modified skill files can contain incorrect, incomplete, or misleading guidance. <br>
Mitigation: Review generated SKILL.md content, bundled references, and scripts before packaging or deploying the skill. <br>
Risk: The packaging helper archives all files under the selected skill directory, which can unintentionally include secrets or unrelated files. <br>
Mitigation: Use an explicit workspace path, inspect the skill directory contents before packaging, and keep secrets outside the skill folder. <br>
Risk: The release is third-party-owned and may be forked or republished under identities that differ from the original source. <br>
Mitigation: Confirm the publisher handle and package identity are acceptable before using the skill in shared or production environments. <br>


## Reference(s): <br>
- [Workflow Patterns](references/workflows.md) <br>
- [Output Patterns](references/output-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional generated skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local skill directories and package them as .skill archives when the user asks.] <br>

## Skill Version(s): <br>
1.3.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
