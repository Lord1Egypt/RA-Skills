## Description: <br>
Provides expanded access to internal knowledge, memory, logs, skills, and analytics for a trusted Telegram group while blocking calendar access outside private chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HellAdventurer](https://clawhub.ai/user/HellAdventurer) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and team operators use this skill to let a trusted Telegram group query OpenClaw workspace knowledge, memory, logs, and assistant workflows while forcing calendar requests into private chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trusted Telegram group members and private-chat users may gain broad access to internal workspace memory, logs, reports, and enabled tools. <br>
Mitigation: Install only for fully trusted groups; add per-user allowlists or role checks, restrict readable paths, and review group membership regularly. <br>
Risk: Execution and server-side hook workflows may be reachable through group requests when the host pipeline enables them. <br>
Mitigation: Keep group requests read-only by default and require confirmation for exec and hook actions. <br>
Risk: Internal logs and memory may expose secrets or sensitive operational details. <br>
Mitigation: Redact secrets from logs and memory before deployment and limit access to users with a clear operational need. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HellAdventurer/spaces-group-assistant) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Telegram-compatible text or Markdown responses from the host assistant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calendar queries are refused outside private chat; trusted group and private-chat requests may pass through to workspace, log, memory, and enabled tool workflows.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence; artifact package.json and _meta.json list 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
