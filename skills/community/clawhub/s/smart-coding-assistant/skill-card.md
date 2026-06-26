## Description: <br>
Smart Coding Assistant routes coding tasks to suitable large language models for code generation, review, debugging, refactoring, testing, documentation, architecture, and technical Q&A. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to classify programming tasks, choose an appropriate model, and produce coding assistance such as code, reviews, debugging guidance, tests, documentation, and configuration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, pasted code, logs, or generated task context may be sent to configured third-party model providers. <br>
Mitigation: Do not include secrets, regulated data, proprietary code, or confidential logs unless the organization has approved the provider and data handling; use scoped API keys with spending controls. <br>
Risk: Generated code, reviews, tests, or debugging guidance may be incorrect or incomplete. <br>
Mitigation: Review outputs before use, run tests and security checks, and require human approval before applying changes to production systems. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/davidme6/smart-coding-assistant) <br>
- [Model Profiles](references/model-profiles.md) <br>
- [Task Taxonomy](references/task-taxonomy.md) <br>
- [Best Practices](references/best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May route tasks across configured third-party model providers using QWEN_API_KEY, DEEPSEEK_API_KEY, or GLM_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
