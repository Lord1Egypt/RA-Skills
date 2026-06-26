## Description: <br>
Manage message queues with priorities and retry logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users use Queue to add, prioritize, track, review, search, and export locally stored queue items for task and workflow management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queue entries can be saved persistently on local disk and later included in exports. <br>
Mitigation: Avoid entering secrets or sensitive operational data, and review ~/.local/share/queue plus exported files before sharing or retaining them. <br>
Risk: The public description may understate the local activity logging and export behavior. <br>
Mitigation: Confirm storage, deletion, and export expectations with the publisher before installing in environments that handle sensitive work. <br>


## Reference(s): <br>
- [Queue on ClawHub](https://clawhub.ai/bytesagain-lab/queue) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Plain text command output with optional JSON, CSV, or text exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local logs under ~/.local/share/queue and writes exports in JSON, CSV, or text format.] <br>

## Skill Version(s): <br>
2.0.1 (source: release evidence and SKILL.md frontmatter; script output reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
