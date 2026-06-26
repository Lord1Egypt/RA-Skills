## Description: <br>
Analyzes a user's local decrypted WeChat database to generate structured personality, communication, relationship, and interest profile reports, then syncs selected updates into an OpenClaw memory layer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengziliang43-cmyk](https://clawhub.ai/user/fengziliang43-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to locally decrypt and analyze their own WeChat data, produce Markdown profile files, and optionally sync selected profile updates into an OpenClaw memory file. It is intended for users who understand the privacy implications of processing sensitive chat-derived data on their own Windows machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes highly sensitive WeChat chat data and can persist derived profile content across local profile files and memory files. <br>
Mitigation: Review generated profile content before use, remove bundled generated profile files, and minimize or delete sensitive chat-derived details before syncing them into MEMORY.md. <br>
Risk: Setup relies on an external WeChat decryptor and administrator privileges to decrypt the local database. <br>
Mitigation: Review the external decryptor before running setup, run it only on data you are authorized to process, and install only if administrator-level local decryption is acceptable. <br>
Risk: Ongoing cron and memory scripts can maintain or expand persisted session-derived content. <br>
Mitigation: Disable the cron and memory maintenance scripts unless ongoing session capture and memory maintenance are explicitly desired. <br>
Risk: The security assessment reports broad persistence and unpinned setup code. <br>
Mitigation: Pin or review downloaded setup dependencies before execution and periodically audit local storage, decrypted data, and memory outputs. <br>


## Reference(s): <br>
- [Skill release page](https://clawhub.ai/fengziliang43-cmyk/ziji-ai) <br>
- [wechat-decrypt repository used by setup](https://github.com/ylytdeng/wechat-decrypt.git) <br>
- [Three-layer memory agent rules](three-layer-memory/references/agents-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files and concise command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates multiple local profile files under storage/cold and may update an OpenClaw MEMORY.md file when sync is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
