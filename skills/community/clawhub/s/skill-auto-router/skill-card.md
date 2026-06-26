## Description: <br>
Automatically discover and route relevant installed skills for the current task, plus run a daily skill audit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chchchadzilla](https://clawhub.ai/user/chchchadzilla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to rank installed skills before a task and to audit skill descriptions for routing quality during daily workspace maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The router scans local skill folders and may print installed skill names, paths, and matching metadata. <br>
Mitigation: Keep scanned roots limited to intended skill directories and review command output before sharing logs. <br>
Risk: Automatic AGENTS or HEARTBEAT hooks can route tasks based on stale or vague skill descriptions. <br>
Mitigation: Run the daily audit, tighten weak descriptions, and load only the top one to three matching skills. <br>


## Reference(s): <br>
- [Setup Checklist for Auto Skill Routing](references/setup-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/chchchadzilla/skill-auto-router) <br>
- [Publisher Profile](https://clawhub.ai/user/chchchadzilla) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output from the router script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pre-task routing returns ranked skill candidates with match reasons; daily audit reports discovered skills, weak descriptions, and high-overlap tokens.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
