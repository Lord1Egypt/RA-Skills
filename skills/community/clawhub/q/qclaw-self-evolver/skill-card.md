## Description: <br>
QClaw Self-Evolver helps an AI agent record corrections, assess skill health, run a Sense-Assess-Evolve review loop, and generate candidate skills from recurring task patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qshan1](https://clawhub.ai/user/qshan1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to add self-improvement workflows to QClaw-style agents, including correction capture, periodic evolution scans, skill health assessment, and candidate skill generation from repeated work patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent background behavior through a recurring SEA evolution cron job. <br>
Mitigation: Review or disable the cron job before enabling the skill, and require explicit approval for scheduled execution. <br>
Risk: The skill stores user correction history under ~/.qclaw/workspace/.learnings, which may capture sensitive context if users include secrets in corrections. <br>
Mitigation: Avoid recording secrets, review retention expectations, and sanitize learning files before sharing or deploying them. <br>
Risk: The skill can generate candidate skills and prompt or behavior changes from recurring patterns. <br>
Mitigation: Require manual review, testing, and rollback planning before generated skills or prompt changes become active. <br>


## Reference(s): <br>
- [QClaw Self-Evolver ClawHub page](https://clawhub.ai/qshan1/qclaw-self-evolver) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON status output, Python-generated files, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent workspace files under ~/.qclaw/workspace and register a recurring SEA evolution cron job.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
