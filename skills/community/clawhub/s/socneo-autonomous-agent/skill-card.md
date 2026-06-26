## Description: <br>
AI Autonomous Agent Framework with self-driven capabilities. Implements perception, judgment, execution, and reflection layers for intelligent autonomous operation. Use when building self-aware, adaptive AI systems that can operate independently while maintaining safety and user control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[socneo](https://clawhub.ai/user/socneo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external builders use this skill to assemble autonomous agents that monitor state, evaluate task priority and risk, execute approved work with recovery, and learn from outcomes while preserving user controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect broad local system state and offers autonomous execution without clearly enforced user controls. <br>
Mitigation: Keep it in assisted or manual mode, define explicit approval rules, and avoid connecting it to sensitive write-capable tools or production credentials. <br>
Risk: Monitoring and memory features can capture more system or user activity than intended. <br>
Mitigation: Define explicit monitored paths, event sources, retention limits, and audit review practices before enabling monitoring. <br>
Risk: Risk-aware autonomous decisions may still be incorrect or overconfident. <br>
Mitigation: Require human approval for medium- and high-risk actions, preserve user override, and keep rollback or recovery procedures available. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/socneo/socneo-autonomous-agent) <br>
- [Skill-declared GitHub repository](https://github.com/Socneo/autonomous-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include configuration thresholds, approval rules, monitoring status, decision rationale, and task execution reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
