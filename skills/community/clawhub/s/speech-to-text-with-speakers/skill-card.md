## Description: <br>
Speech To Text With Speakers lets agents transcribe audio from a file ID or HTTPS URL into text, SRT, WebVTT, or JSON with optional speaker labels and word timestamps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent transcribe meetings, interviews, podcasts, webinars, voice memos, and videos through AgentPMT-hosted speech-to-text tool calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio files and public media URLs submitted for transcription may contain confidential, regulated, personal, or third-party content. <br>
Mitigation: Install and use the skill only when authorized to send the selected audio or URL to AgentPMT-hosted transcription workflows, and review provider privacy, retention, logging, and billing terms before use. <br>
Risk: Transcription may involve downstream speech-to-text providers and can produce sensitive transcript text, subtitles, timestamps, or speaker labels. <br>
Mitigation: Keep inputs scoped to the minimum content needed, avoid placing secrets in prompts or logs, and handle returned transcripts and subtitle files as sensitive data. <br>


## Reference(s): <br>
- [Speech To Text With Speakers on ClawHub](https://clawhub.ai/agentpmt/skills/speech-to-text-with-speakers) <br>
- [AgentPMT Speech To Text With Speakers](https://www.agentpmt.com/marketplace/speech-to-text-with-speakers) <br>
- [Speech To Text With Speakers Schema](schema.md) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Text, Markdown, JSON] <br>
**Output Format:** [Markdown instructions with JSON tool-call examples; remote calls can return text, SRT, WebVTT, or JSON transcripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill supports quick, standard, and extended transcription tiers for recordings up to 15, 30, or 60 minutes, with optional diarization, word timestamps, profanity filtering, and alternative transcripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
