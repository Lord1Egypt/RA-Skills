## Description: <br>
Guides agents through creating or updating effective skills with structured workflows, resource organization, and packaging guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yixinli867](https://clawhub.ai/user/yixinli867) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create or update agent skills by defining use cases, selecting bundled resources, writing SKILL.md, and packaging the result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may direct an agent to run helper scripts that are not included in the artifact. <br>
Mitigation: Before following script commands, confirm the intended init_skill.py and package_skill.py locations and avoid executing similarly named scripts from unrelated directories. <br>
Risk: Generated or modified skills could contain incorrect instructions or weak guardrails. <br>
Mitigation: Review generated skill files and run normal validation and security scanning before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to create files and run local helper scripts when those scripts are available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
