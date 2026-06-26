## Description: <br>
Skill Orchestra routes agent tasks using skill demands, competence scores, performance history, and cost trade-offs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobisamaa](https://clawhub.ai/user/tobisamaa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to select suitable downstream skills or agents for a task while balancing expected performance, cost, and routing diversity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Routing decisions can be imprecise and may select a less suitable downstream skill or agent. <br>
Mitigation: Review routing recommendations before acting on them and keep normal approvals enabled for downstream skills, especially skills that can automate desktop actions, post publicly, modify data, or store memory. <br>
Risk: Routing history or pattern-learning data can retain task prompts or context if persistence is enabled. <br>
Mitigation: Avoid persisting raw prompts unless retention limits and redaction controls are in place. <br>


## Reference(s): <br>
- [ClawHub Skill Orchestra release page](https://clawhub.ai/tobisamaa/skill-orchestra) <br>
- [SkillOrchestra research code referenced by artifact](https://github.com/jiayuww/SkillOrchestra) <br>
- [arXiv:2602.19672](https://arxiv.org/abs/2602.19672) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, Python dictionary results, and CLI-style command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return selected skill names, routing explanations, candidate rankings, and success or error dictionaries.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
