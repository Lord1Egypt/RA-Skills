## Description: <br>
Securely share files using encrypted, expiring vnsh.dev links with the vnsh CLI for uploading and decrypting shared content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raullenchai](https://clawhub.ai/user/raullenchai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to upload local files or command output to encrypted, expiring vnsh.dev links and to decrypt vnsh.dev links into local temporary files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload logs, diffs, source code, credentials, or conversation context to an external file-sharing service. <br>
Mitigation: Require user confirmation before uploads and review or redact content before sharing. <br>
Risk: The skill can automatically fetch and decrypt vnsh links, which may expose untrusted or unexpected content to the agent workflow. <br>
Mitigation: Ask before opening vnsh links and inspect downloaded files before further processing. <br>
Risk: The documented installer uses an unpinned remote shell command. <br>
Mitigation: Inspect the installer or replace it with a verified installation path before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/raullenchai/vnsh) <br>
- [vnsh website](https://vnsh.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with inline shell commands and generated vnsh.dev URLs or local decrypted file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce encrypted, expiring external file-sharing links and temporary decrypted local files.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
