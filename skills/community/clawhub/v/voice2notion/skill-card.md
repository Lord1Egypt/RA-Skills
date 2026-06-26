## Description: <br>
语音录音转录并保存到 Notion 数据库。使用 faster-whisper 转录，自动提取关键信息并写入数据库。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JiabaoChen1](https://clawhub.ai/user/JiabaoChen1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and personal productivity users use this skill to transcribe voice recordings with faster-whisper, polish and extract key information, and save the resulting notes, tasks, and recording links to a Notion database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Notion integration can access the target database. <br>
Mitigation: Use a dedicated Notion integration scoped only to the intended database. <br>
Risk: The Notion API key is stored locally and could expose database access if shared. <br>
Mitigation: Keep the API key private, do not commit it to public repositories, and rotate it periodically. <br>
Risk: Public recording links may expose sensitive audio content. <br>
Mitigation: Use public audio links only when the recording is safe to share publicly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JiabaoChen1/voice2notion) <br>
- [Notion database template](https://www.notion.so/4e667ba767e2414a9f89041471d5f85d) <br>
- [Notion integrations](https://www.notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples, Python snippets, configuration steps, and Notion database field guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to transcribe a user-provided audio file, extract structured notes, and create or update Notion database records.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
