## Description: <br>
Stop waiting for prompts. Keep working. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayakolin](https://clawhub.ai/user/ayakolin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up a task queue, proactive heartbeat routine, and operating practices that help agents continue approved work between human prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled autonomous work can continue with weak safety boundaries if the queue contains unapproved or sensitive tasks. <br>
Mitigation: Restrict the task queue to human-approved work, limit writable paths and external actions, and require approval for sensitive or destructive tasks. <br>
Risk: Frequent heartbeats and status reporting can expose private data if agents write secrets or sensitive context into memory files or team channels. <br>
Mitigation: Disable automatic team-channel posting unless the channel is approved, and instruct agents not to log secrets or private data. <br>
Risk: Autonomous task selection can drift away from current human priorities. <br>
Mitigation: Keep human requests first, maintain explicit Ready/In Progress/Blocked/Done queue states, and escalate blockers before continuing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ayakolin/temp-agent-autonomy-kit) <br>
- [Artifact README](artifact/README.md) <br>
- [Task Queue Template](artifact/templates/QUEUE.md) <br>
- [Heartbeat Template](artifact/templates/HEARTBEAT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces task queue and heartbeat guidance for agent operation; the artifact contains documentation and templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
