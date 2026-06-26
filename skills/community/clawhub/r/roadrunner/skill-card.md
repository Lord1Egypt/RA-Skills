## Description: <br>
Beeper Desktop CLI for chats, messages, contacts, connect info, websocket events, search, and reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johntheyoung](https://clawhub.ai/user/johntheyoung) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Roadrunner to let an agent operate Beeper Desktop through the local rr CLI for chat lookup, message search, contact resolution, reminders, focus workflows, and explicitly requested message actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The rr CLI can access Beeper chats, contacts, messages, and account state. <br>
Mitigation: Install only when the user trusts Roadrunner and is comfortable granting Beeper account access; keep requests narrow and prefer readonly or agent modes for lookups. <br>
Risk: Write-capable commands can send, edit, react to, archive, create, or otherwise change Beeper data. <br>
Mitigation: Use mutating commands only after the user gives explicit recipient and content details, and use dry-run validation when available before write actions. <br>
Risk: Raw command output may expose private chat lists, message contents, identifiers, or tokens. <br>
Mitigation: Summarize only the information needed by the user, avoid pasting raw JSON dumps into messages, and never request, paste, or store raw authentication tokens. <br>


## Reference(s): <br>
- [Roadrunner on ClawHub](https://clawhub.ai/johntheyoung/roadrunner) <br>
- [Roadrunner homepage](https://github.com/johntheyoung/roadrunner) <br>
- [Go install module](github.com/johntheyoung/roadrunner/cmd/rr@v0.17.0) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON or JSONL output handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers readonly and agent modes for lookups; mutating commands require explicit user intent.] <br>

## Skill Version(s): <br>
0.17.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
