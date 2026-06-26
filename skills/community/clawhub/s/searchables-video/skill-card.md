## Description: <br>
YouTube, Bilibili, and local video search, analysis, Q&A, summarization, highlights, and article generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dejavukong](https://clawhub.ai/user/dejavukong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to connect an agent to the Searchables desktop app for searching private video libraries, analyzing YouTube, Bilibili, and local videos, generating summaries, Q&A responses, highlights, articles, and optional Notion exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can search a user's private indexed video library for loosely related video requests. <br>
Mitigation: Ask for explicit user confirmation before searching private library content or using results from private videos. <br>
Risk: The skill depends on trusting the Searchables desktop app and local API with video library data, local file paths, and browser-login-backed platform access. <br>
Mitigation: Keep the API bound to localhost unless another host is intentionally trusted, and install only when the Searchables desktop app is trusted. <br>
Risk: Video processing and exports can spend credits or send transcripts and notes to Notion. <br>
Mitigation: Require explicit confirmation before processing videos, processing local files, spending credits, or exporting content to Notion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dejavukong/searchables-video) <br>
- [Publisher profile](https://clawhub.ai/user/dejavukong) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with curl commands and API-derived JSON summaries or citations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include video timestamps, source quotes, generated summaries, highlights, articles, subtitle text, and Notion export links.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
