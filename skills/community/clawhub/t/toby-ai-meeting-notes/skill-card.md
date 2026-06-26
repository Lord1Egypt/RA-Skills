## Description: <br>
Transcribe and summarize meetings, choose an AI model for the task, and call SkillBoss with a SkillBoss API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to set up SkillBoss-backed meeting transcription and summarization workflows, select an appropriate model, and produce meeting notes from external AI APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup and API key scope are broader than meeting transcription and summarization. <br>
Mitigation: Prefer manual setup limited to the needed workflow, and use a restricted or budget-limited SkillBoss key if available. <br>
Risk: The one-command setup fetches remote configuration. <br>
Mitigation: Inspect the remote setup file before allowing one-command configuration. <br>
Risk: Meeting content may include confidential or regulated information. <br>
Mitigation: Avoid sending sensitive meeting content unless external processing by SkillBoss and downstream model providers is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobeyrebecca/toby-ai-meeting-notes) <br>
- [SkillBoss setup file](https://skillboss.co/skill.md) <br>
- [SkillBoss console](https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=ai-meeting-notes) <br>
- [SkillBoss chat completions endpoint](https://api.skillboss.co/v1/chat/completions) <br>
- [SkillBoss products](https://skillboss.co/products) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and OpenAI-compatible API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may send meeting content to SkillBoss and downstream model providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
