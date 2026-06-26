## Description: <br>
Automatically archives OpenClaw conversation messages, operation records, and token usage metadata to a local SQLite database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18940111404](https://clawhub.ai/user/18940111404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and plugin developers use this skill to retain searchable local records of chat messages, operations, and usage statistics for later review or integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin saves full conversation content and usage metadata in a local SQLite database. <br>
Mitigation: Treat the database as sensitive, restrict local file access, consider backup retention, and avoid using it for chats containing secrets unless long-term local storage is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18940111404/zhujian-session-archive) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Configuration, Usage metadata] <br>
**Output Format:** [SQLite database records with optional JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores conversation content, operation records, token usage, timestamps, channels, message types, and related metadata locally.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
