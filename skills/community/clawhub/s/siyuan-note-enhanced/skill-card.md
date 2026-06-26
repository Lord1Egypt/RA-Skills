## Description: <br>
思源笔记读写技能，提供与思源笔记（SiYuan Note）进行交互的能力，包括读取和写入笔记内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jueduilunhui](https://clawhub.ai/user/jueduilunhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to read, search, create, clip, and synchronize content with a SiYuan Note workspace through the SiYuan API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist full conversations or clipped content into a SiYuan workspace, which may include secrets or personal data. <br>
Mitigation: Review content before syncing, avoid syncing sensitive conversations, and use only a SiYuan instance you control. <br>
Risk: The skill requires a SiYuan API token and includes credential-handling patterns in debug and test files. <br>
Mitigation: Prefer SIYUAN_API_TOKEN, avoid plaintext token configuration, and rotate or ignore any shipped hardcoded or sample token. <br>
Risk: Write and verification scripts can create or modify notes when executed. <br>
Mitigation: Run write and verification scripts only when you intentionally want notes created in your workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jueduilunhui/siyuan-note-enhanced) <br>
- [SiYuan Chrome extension reference](https://github.com/siyuan-note/siyuan-chrome) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell examples, plus SiYuan API operations when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, a running SiYuan instance, and SIYUAN_API_TOKEN for authenticated operations.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata, _meta.json, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
