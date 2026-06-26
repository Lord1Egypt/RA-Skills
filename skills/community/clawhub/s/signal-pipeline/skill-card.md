## Description: <br>
Marketing intelligence pipeline - gather signals from RSS, X/Twitter, Telegram, and Gmail newsletters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mephistophelesbits](https://clawhub.ai/user/mephistophelesbits) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, marketers, and content teams use this skill to build a content intelligence workflow that collects marketing and technology signals from RSS, X/Twitter, Telegram, and Gmail newsletters. It supports daily draft posts, weekly summaries, monthly deep-dives, trend tracking, competitive intelligence, and personal-branding research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Gmail newsletters and external RSS, X/Twitter, and Telegram sources, which may expose or collect sensitive source data. <br>
Mitigation: Use a dedicated newsletter mailbox or tightly scoped Gmail setup, confirm enabled sources before running, and review collected records before sharing generated outputs. <br>
Risk: Collected data is stored locally in SQLite databases and daily JSON signal files. <br>
Mitigation: Confirm database and output paths before installation, restrict filesystem access, and delete stored data when it is no longer needed. <br>
Risk: Newsletter search uses shell command construction around Gmail queries. <br>
Mitigation: Fix command construction before accepting configurable queries, and avoid untrusted query input until the command invocation is hardened. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mephistophelesbits/signal-pipeline) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python scripts, shell commands, SQLite databases, JSON daily signal files, and stdout reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily signal files are written as JSON; weekly and monthly reports are printed to stdout; source records are stored in local SQLite databases.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
