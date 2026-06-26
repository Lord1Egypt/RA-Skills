## Description: <br>
Extracts local same-day agent conversation logs so an agent can summarize them into a daily memory note. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pazzilivo](https://clawhub.ai/user/pazzilivo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to collect local OpenClaw session messages for a chosen date and turn them into a concise daily memory summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly collects daily local agent conversation logs and writes raw chat excerpts to a predictable temporary plaintext file. <br>
Mitigation: Use it only for selected agents or non-sensitive sessions where possible, restrict access to the temporary transcript, and remove or protect the transcript after summarization. <br>
Risk: Daily summaries may become long-lived memory containing sensitive or unintended conversation details. <br>
Mitigation: Review the generated summary before saving it to memory and avoid running the skill on sensitive work. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pazzilivo/session-digest) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Plain text transcript extraction and Markdown daily summary template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local OpenClaw agent sessions and writes /tmp/session-digest-YYYY-MM-DD.txt before the agent creates memory/YYYY-MM-DD.md.] <br>

## Skill Version(s): <br>
4.1.3 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
