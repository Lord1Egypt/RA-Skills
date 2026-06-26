## Description: <br>
CLI skill for Telegram to sync chats, search messages, filter keywords, and monitor groups from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackwener](https://clawhub.ai/user/jackwener) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers, operators, and AI agents use this skill to authenticate with a user-controlled Telegram account, refresh a local Telegram message cache, search or filter chat history, export results, monitor new messages, and explicitly send Telegram messages from the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local CLI with access to the user's Telegram account and can store chat contents on disk. <br>
Mitigation: Install only for trusted local environments, protect the data and session directory, avoid shared machines, and avoid exposing session files or cached messages in agent logs. <br>
Risk: Exports and machine-readable command output may contain private Telegram message content. <br>
Mitigation: Review exported files and agent transcripts before sharing them, and limit exports to the minimum chat and time window needed. <br>
Risk: `tg send` sends a real outbound Telegram message and `tg purge -y` irreversibly deletes the local cached copy. <br>
Mitigation: Require explicit user confirmation for send and purge operations, and treat purge as local-cache deletion rather than Telegram-side deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackwener/tg-cli) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jackwener) <br>
- [Structured Output Schema](artifact/SCHEMA.md) <br>
- [PyPI package](https://pypi.org/project/kabi-tg-cli/) <br>
- [Telegram app credentials](https://my.telegram.org/apps) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, YAML, JSON, Files, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands; CLI command output may be rich text, YAML, JSON, or exported text/YAML/JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Machine-readable CLI output uses a shared success/error envelope documented in SCHEMA.md; non-TTY stdout defaults to YAML.] <br>

## Skill Version(s): <br>
0.4.1 (source: release evidence, pyproject.toml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
