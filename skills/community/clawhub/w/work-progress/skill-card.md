## Description: <br>
Work Progress monitors OpenClaw work progress, todo items, sub-agent timeouts or missing sessions, and full-session status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amd5](https://clawhub.ai/user/amd5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor OpenClaw work sessions, surface stalled or failed tasks, check daily todos, and receive recovery guidance for interrupted work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect active sessions across all OpenClaw agents and retain local session and task metadata. <br>
Mitigation: Install only where that monitoring scope is acceptable; review configured cron jobs and clear the local state file when historical monitoring data should not be retained. <br>
Risk: Automated progress and recovery reports may flag stale, failed, or missing sessions and write local recovery notes. <br>
Mitigation: Review reported issues before acting on recovery guidance, especially before rerunning interrupted work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amd5/work-progress) <br>
- [Publisher profile](https://clawhub.ai/user/amd5) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance, files] <br>
**Output Format:** [Plain text or JSON monitoring reports; local Markdown and JSON state files may be updated.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs NO_REPLY when no action is needed; may retain local task state and append recovery notes to local memory.] <br>

## Skill Version(s): <br>
4.0.6 (source: frontmatter, skill.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
