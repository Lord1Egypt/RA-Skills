## Description: <br>
XiaChat CLI supports SOUL profile management, personality matching, AI avatar pre-chat, and Soul Square persona chat from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lizhijun](https://clawhub.ai/user/lizhijun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate XiaChat personality workflows from a command line, including creating SOUL profiles, finding matches, starting avatar pre-chat sessions, and chatting with Soul Square personas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SOUL profiles, chat exports, match data, and pre-chat content may contain sensitive personal information sent to an external service. <br>
Mitigation: Install only if the XiaChat service is trusted, review chat logs before import, and avoid sending content that should not leave the user's environment. <br>
Risk: The CLI requires an API key that could be exposed through shell history, shared files, or commits. <br>
Mitigation: Use a revocable API key, store it in an environment variable or secret manager, and avoid committing or sharing it. <br>
Risk: Export commands may overwrite local SOUL profile files or write sensitive data to unintended paths. <br>
Mitigation: Review output paths before export and keep generated profile files in appropriate protected locations. <br>


## Reference(s): <br>
- [XiaChat](https://xiachat.com) <br>
- [XiaChat API Settings](https://xiachat.com/settings/api) <br>
- [Soul Square](https://xiachat.com/square) <br>
- [SOUL Profiles](https://xiachat.com/soul) <br>
- [XiaChat Matching](https://xiachat.com/match) <br>
- [ClawHub Skill Page](https://clawhub.ai/lizhijun/xiachat-cli) <br>
- [Publisher Profile](https://clawhub.ai/user/lizhijun) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown with inline shell commands and CLI usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes JSON-oriented CLI workflows and API key configuration notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
