## Description: <br>
Self-Improvement Engine for AI agents that records mistakes, turns them into behavior rules, and uses them to reduce repeated errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aptratcn](https://clawhub.ai/user/aptratcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to help an AI agent log mistakes, derive durable working rules, and check those rules before repeating similar work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to maintain long-lived mistake logs and behavior rules that may retain sensitive user content or incorrect lessons. <br>
Mitigation: Review memory/mistakes.json and WORK_RULES.md regularly, keep sensitive content out of logs, and require explicit confirmation before converting a correction into a permanent rule. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aptratcn/xiaobai-self-improve) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON examples and shell command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update memory/mistakes.json and WORK_RULES.md when adopted by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
