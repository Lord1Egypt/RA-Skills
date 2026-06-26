## Description: <br>
WorkCRM is a local-first OpenClaw CRM skill that drafts contact, activity, and task updates and writes them only after explicit user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[extraterrest](https://clawhub.ai/user/extraterrest) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and OpenClaw users use WorkCRM to turn chat notes into auditable local CRM drafts, then confirm or reject each proposed write before records are saved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local CRM records and draft history may contain sensitive business or personal information. <br>
Mitigation: Choose the SQLite database location deliberately, protect the local data directory, and avoid storing sensitive records on shared or unmanaged machines. <br>
Risk: Drafted CRM changes could be incorrect if the source chat note is ambiguous. <br>
Mitigation: Review each draft before replying with the explicit confirmation token that commits the write. <br>


## Reference(s): <br>
- [ClawHub Workcrm release page](https://clawhub.ai/extraterrest/workcrm) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Plain text user messages and JSON payloads for drafts, pending actions, and write results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit confirmation before saving CRM records; stores local SQLite data and draft history.] <br>

## Skill Version(s): <br>
0.1.0-alpha.4 (source: server release evidence and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
