## Description: <br>
Smart Meeting Assistant automates meeting audio transcription, structured meeting summary generation, and action item extraction from recordings or transcripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and developers can use this skill to turn meeting recordings or prepared transcripts into transcripts, meeting minutes, and action-item lists. It is intended for post-meeting documentation workflows that rely on the configured AstronClaw API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting recordings and transcripts are sent to the configured AstronClaw API endpoint. <br>
Mitigation: Use the skill only when provider terms, retention behavior, participant consent, and meeting confidentiality requirements are acceptable. <br>
Risk: The skill requires a sensitive API credential and supports a configurable API base URL. <br>
Mitigation: Protect ASTRONCLAW_API_KEY and verify ASTRONCLAW_API_BASE before processing recordings or transcripts. <br>


## Reference(s): <br>
- [AstronClaw API Reference](references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Text transcripts, Markdown meeting summaries, JSON todo lists, and shell-oriented usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write transcript, summary, and todo files with timestamped names when the full pipeline is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
