## Description: <br>
Session Archive automatically saves OpenClaw conversation messages, operation records, and token usage data to a local SQLite database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18940111404](https://clawhub.ai/user/18940111404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users install this plugin when they need local session archiving, usage accounting, and queryable records of messages, operations, and token usage. It is useful for audit, troubleshooting, and usage analysis when local retention of conversation data is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin automatically saves full conversation content and metadata to a local SQLite database. <br>
Mitigation: Install only where local retention is intended, protect the configured database path, and define deletion, retention, backup, and encryption controls appropriate for the data being archived. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18940111404/session-archive) <br>
- [Publisher profile](https://clawhub.ai/user/18940111404) <br>
- [README](README.md) <br>
- [Plugin manifest](openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Configuration, Shell commands, Guidance] <br>
**Output Format:** [SQLite database records plus Markdown documentation and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes messages, operations, and token usage to a local SQLite database; default path is ~/.openclaw/session-archive.db.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
