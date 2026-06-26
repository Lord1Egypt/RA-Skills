## Description: <br>
Self-improving agent system for OpenClaw that detects workspace errors, selects improvement topics, creates research and backlog items, records impact, and remembers useful procedures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mopga](https://clawhub.ai/user/mopga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to turn OpenClaw error logs, circuit-breaker state, and backlog patterns into prioritized improvement tasks, research notes, and impact measurements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically turn workspace errors into persistent future agent work without clear approval boundaries. <br>
Mitigation: Keep cron or auto-trigger execution disabled until generated research files and backlog tasks have been reviewed. <br>
Risk: The skill reads logs and writes memory, backlog, and impact files in the configured workspace. <br>
Mitigation: Restrict workspace write access and avoid storing secrets in logs or memory files that the skill reads. <br>
Risk: Generated tasks may cause later agents to make changes based on incomplete or stale error analysis. <br>
Mitigation: Require human review before any agent executes generated tasks and re-check the current workspace state first. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research and backlog entries, JSON logs, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to the configured OpenClaw workspace, including memory, backlog, research, trigger, and impact files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
