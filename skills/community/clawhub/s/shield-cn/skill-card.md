## Description: <br>
Shield CN provides localized security checks for Chinese-language AI agent workflows, including prompt-injection, data-leak, credential-leak, and DingTalk, Feishu, and WeChat-related detections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Shield CN to scan selected workspaces, check Chinese-language inputs for suspicious prompt-injection or phishing patterns, and generate local security audit reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local audit script scans the workspace selected by the user and can save reports or logs under ~/.openclaw. <br>
Mitigation: Scan only intended project directories, avoid scanning an entire home directory unless deliberate, and review or delete local reports and logs when finished. <br>
Risk: Block mode is a helper control and may not stop every unsafe action or false positive. <br>
Mitigation: Treat block mode as advisory, keep human review in the workflow, and do not rely on it as the only enforcement control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/shield-cn) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, console text, JSON-like check results, Python code examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Security audit reports and guard logs are written locally for the workspace selected by the user.] <br>

## Skill Version(s): <br>
2284.0.0 (source: server release metadata; artifact metadata reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
