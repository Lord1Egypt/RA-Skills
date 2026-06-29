## Description: <br>
Transcribes Telegram voice notes into text before the assistant replies, so the agent can answer the transcript as the user's message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aditya0320](https://clawhub.ai/user/aditya0320) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Telegram assistant users and operators use this skill to convert inbound voice notes into text before an agent replies. It is intended for Windows OpenClaw deployments configured with Google Cloud Speech-to-Text credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram voice notes are sent through Google Cloud and related OpenClaw/Dialogflow infrastructure for transcription and response handling. <br>
Mitigation: Use a limited service account, avoid sensitive voice content unless retention and consent requirements are met, and review cloud data-handling policies before deployment. <br>
Risk: Broad trigger wording could cause the transcription workflow to activate in more Telegram voice-note contexts than intended. <br>
Mitigation: Tighten trigger wording and deployment scope before broad rollout. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aditya0320/telegram-voice-stt) <br>
- [ClawHub publisher profile: aditya0320](https://clawhub.ai/user/aditya0320) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces transcript-aware response guidance for Telegram voice-note workflows; no bundled executable code is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
