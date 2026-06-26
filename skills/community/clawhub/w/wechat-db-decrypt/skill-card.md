## Description: <br>
Guides an agent through reading, searching, and extracting messages from already decrypted WeChat PC 3.x and 4.x SQLite databases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[as1113435](https://clawhub.ai/user/as1113435) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and investigators use this skill to inspect decrypted local WeChat databases they own or are explicitly authorized to process. It helps locate message tables, run keyword searches, and export relevant message snippets for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be used to mine private WeChat messages or group chats without adequate consent. <br>
Mitigation: Use it only for data the operator owns or is explicitly authorized to process, and avoid customer, competitor, group, or third-party chat mining without clear consent. <br>
Risk: Unverified decryptor executables or live-session key extraction can expose credentials or active WeChat sessions. <br>
Mitigation: Avoid running unverified decryptor executables against live sessions; prefer reviewed tooling and work from decrypted database copies rather than active application state. <br>
Risk: Extracted messages and derived analysis can become persistent sensitive records. <br>
Mitigation: Apply retention limits, access controls, and deletion controls before saving logs, JSON exports, or derived analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/as1113435/wechat-db-decrypt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included Python example can write local text logs and JSON search results when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
