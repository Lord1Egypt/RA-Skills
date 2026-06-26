## Description: <br>
Use when a user pastes a meeting transcript and needs a structured summary with action items and decision owners. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjipeng977](https://clawhub.ai/user/wangjipeng977) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external collaborators, developers, and project teams use this skill to convert pasted meeting transcripts into concise summaries with decisions, action items, assignees, deadlines when stated, and unresolved open items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting transcripts may contain secrets, regulated personal data, or confidential internal discussions. <br>
Mitigation: Use the skill only with transcripts the user is authorized to process, and avoid pasting sensitive or regulated content unless the agent session is approved for that data. <br>
Risk: The README mentions API-key and write-mode usage without enough detail to confirm what service is used or where outputs are written. <br>
Mitigation: Before using any API key or write mode, confirm the service, whether transcript text leaves the environment, and where generated outputs are stored. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/wangjipeng-meeting-transcript-to-summary) <br>
- [Metadata source: MiniMax-AI skills](https://github.com/MiniMax-AI/skills) <br>
- [Skill references index](artifact/references/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown structured summary with sections for summary, decisions, action items, and open items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include uncertainty notes, missing-section statements, speaker-label assumptions, and follow-up questions for ambiguous transcripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata; artifact frontmatter and changelog report 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
