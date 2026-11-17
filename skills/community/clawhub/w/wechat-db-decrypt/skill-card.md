## Description:

Guides agents through WeChat PC 3.x/4.x database handling and provides Python examples for searching already decrypted xwechat_files SQLite message databases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[as1113435](https://clawhub.ai/user/as1113435)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to locate WeChat PC database files, assess whether they are decrypted, and query or export messages from decrypted SQLite databases for backup or authorized analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed around decrypted WeChat databases and can expose private chat content.

Mitigation: Use only with data the user owns or is explicitly authorized to process, and minimize retention of extracted messages.

Risk: The artifact discusses unverified external executables and live-process key extraction.

Mitigation: Avoid unverified binaries, prefer reviewed tooling, and isolate any local analysis environment.

Risk: Example behavior can persist chat-derived output in plaintext log or JSON files.

Mitigation: Store outputs only with a clear retention and consent plan, and delete or protect exported results after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/as1113435/skills/wechat-db-decrypt)
- [Publisher profile](https://clawhub.ai/user/as1113435)
- [WeChat database skill source](artifact/SKILL.md)
- [Example message search script](artifact/scripts/search_messages.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and SQL snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local SQLite queries and, when scripts are run, produce plaintext log and JSON search-result files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
