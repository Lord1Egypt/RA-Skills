## Description: <br>
Windows Thunder download client via COM interface for adding, committing, canceling, and managing download tasks programmatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users on Windows use this skill to control a local Thunder/Xunlei client through Python and the Thunder COM interface. It supports adding download tasks, supplying optional headers, committing tasks, canceling active tasks, and checking task state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add network download tasks and write downloaded files to local disk through the Thunder/Xunlei client. <br>
Mitigation: Review each URL, destination path, and expected file size before committing a task. <br>
Risk: Optional custom headers, including cookies, may be sent to the download source. <br>
Mitigation: Avoid real session cookies or sensitive headers unless the destination is trusted and the disclosure is intended. <br>
Risk: The skill depends on Windows COM automation and a locally installed Thunder/Xunlei client. <br>
Mitigation: Use it only on Windows systems where the Thunder client is installed and COM registration is trusted. <br>


## Reference(s): <br>
- [Thunder/Xunlei official site](https://www.xunlei.com/) <br>
- [ClawHub package page](https://clawhub.ai/534422530/thunder-core) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-only; requires Python, pywin32, an installed Thunder/Xunlei client, and local review of download URLs, save paths, and optional headers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
