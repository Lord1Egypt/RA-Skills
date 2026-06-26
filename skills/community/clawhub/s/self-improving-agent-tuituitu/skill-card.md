## Description: <br>
Helps an agent learn from feedback, mistakes, and completed tasks by reflecting on lessons and updating memory or behavior files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[UNCLEKIMWOOD](https://clawhub.ai/user/UNCLEKIMWOOD) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to guide an agent through self-reflection after feedback, errors, or completed work, and to record durable lessons in memory files. It is intended for agents that maintain persistent notes about user preferences, mistakes, and workflow improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages persistent memory updates and broad edits to behavior files, which could record sensitive details or alter future agent behavior without enough oversight. <br>
Mitigation: Require explicit approval and a visible diff before every write, keep secrets and sensitive personal details out of memory, and restrict writes to known memory files. <br>
Risk: The skill mentions modifying AGENTS.md, SOUL.md, cron jobs, or other behavior/control files. <br>
Mitigation: Do not allow edits to behavior or control files unless the user intentionally approves that separate change. <br>


## Reference(s): <br>
- [Self-Improvement Reference](references/improvement-tracking.md) <br>
- [ClawHub skill page](https://clawhub.ai/UNCLEKIMWOOD/self-improving-agent-tuituitu) <br>
- [Publisher profile](https://clawhub.ai/user/UNCLEKIMWOOD) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with memory-file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prompt the agent to propose edits to persistent memory and behavior files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
