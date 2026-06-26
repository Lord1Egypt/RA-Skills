## Description: <br>
Monitor websites for changes, downtime, or specific content, and report when a page changes, goes down, or matches or stops matching a pattern. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zacjiang](https://clawhub.ai/user/zacjiang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run lightweight uptime, change, and content checks for websites, either on demand, from a URL list, or on a recurring OpenClaw cron. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitored page text may be stored locally when change detection is enabled. <br>
Mitigation: Use a private state directory and avoid monitoring sensitive URLs or pages whose content should not be retained locally. <br>
Risk: Recurring checks can create automated network traffic to target websites. <br>
Mitigation: Add a cron schedule only when recurring checks are intended, and choose an interval appropriate for the monitored sites. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zacjiang/site-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/zacjiang) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI exit codes distinguish unchanged or up, changed or not found, and down or error states; watch and batch modes store page text snapshots locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
