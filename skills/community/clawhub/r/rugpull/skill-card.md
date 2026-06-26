## Description: <br>
Provides a shell-based local note and configuration store for rugpull-related entries, with commands to add, list, search, export, remove, and view stats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers or analysts can use this skill to record and manage local notes about rugpull topics. It should not be relied on as an automated blockchain security or protocol-risk analyzer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is advertised as rugpull analysis, but the artifacts show local note/config behavior instead. <br>
Mitigation: Treat it as a local record-keeping utility and do not rely on it for blockchain security analysis or investment decisions. <br>
Risk: Entries are persisted on disk and may contain sensitive wallet, incident, credential, or investigation details. <br>
Mitigation: Avoid entering sensitive information unless local persistence is acceptable; set RUGPULL_DIR to an appropriate private location when used. <br>
Risk: Stored entries can be exported or deleted without recovery safeguards. <br>
Mitigation: Review export destinations and keep separate backups before using remove operations on important records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/rugpull) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/xueyetianya) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; script output is plain text with JSONL or CSV export files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists entries under RUGPULL_DIR, defaulting to ~/.rugpull, and can export or delete stored entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
