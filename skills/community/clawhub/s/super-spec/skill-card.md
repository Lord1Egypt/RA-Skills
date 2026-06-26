## Description: <br>
Super Spec guides agents through a Chinese-language fusion workflow that checks for Superpowers and spec-kit dependencies and walks developers through planning, specification, TDD, debugging, review, and branch completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haoy2025](https://clawhub.ai/user/haoy2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to launch a guided software-development process that combines Superpowers quality workflows with spec-kit's specification-driven steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on separately installed Superpowers and spec-kit skills, so dependency behavior is outside this release. <br>
Mitigation: Review the linked dependency repositories and the files copied into `.claude/skills/` before relying on the workflow. <br>
Risk: Broad prompts such as "start" or "continue" could be interpreted as workflow commands when the skill is invoked unintentionally. <br>
Mitigation: Invoke the skill explicitly, such as with `/super-spec`, and confirm the intended entry point before following workflow guidance. <br>


## Reference(s): <br>
- [Super Spec on ClawHub](https://clawhub.ai/haoy2025/super-spec) <br>
- [super-spec GitHub link listed in skill metadata](https://github.com/haoy2025/super-spec) <br>
- [Superpowers dependency](https://github.com/obra/superpowers) <br>
- [spec-kit dependency](https://github.com/github/spec-kit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with slash-command references and installation links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language workflow launcher; no code execution or credential handling declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
