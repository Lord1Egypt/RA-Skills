## Description: <br>
Skill 质量测评工具，基于 SkillsBench 方法论对 Agent Skills 进行静态文档分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gloreasu](https://clawhub.ai/user/gloreasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to review Agent Skill documentation quality, trigger accuracy, structural completeness, and resource organization before release or comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes a dynamic-testing reference that could be mistaken for normal workflow. <br>
Mitigation: Use the skill for static review of intended Skill files only; do not run commands, use credentials, or follow dynamic-testing steps without a separate sandboxed workflow and explicit user confirmation. <br>


## Reference(s): <br>
- [Evaluation Guidelines](references/evaluation-guidelines.md) <br>
- [Dynamic Testing Guide](references/dynamic-testing-guide.md) <br>
- [SkillsBench](https://www.skillsbench.ai/) <br>
- [SkillsBench Paper](https://arxiv.org/abs/2602.12670) <br>
- [SkillsBench GitHub](https://github.com/benchflow-ai/skillsbench) <br>
- [ClawHub Skill Page](https://clawhub.ai/gloreasu/skill-ce-shi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown evaluation report with scores, findings, and improvement guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static documentation analysis only; no code execution is required for normal use.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
