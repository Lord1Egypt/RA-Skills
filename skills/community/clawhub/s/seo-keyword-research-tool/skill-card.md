## Description: <br>
Automatically fetches YouTube video subtitles and prepares concise summaries for users who need key points from talks, lectures, interviews, or other public videos with captions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[potatosolo](https://clawhub.ai/user/potatosolo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, students, and content curators use this skill to fetch public YouTube captions, format transcript text, and generate structured summaries with executive summaries, key points, and optional detailed notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The marketplace display name suggests SEO keyword research, but the artifact implements YouTube transcript fetching and summarization. <br>
Mitigation: Install and use this release only when a YouTube transcript summarization helper is intended. <br>
Risk: Fetched video captions are untrusted content and may contain text that attempts to steer an agent away from the user's task. <br>
Mitigation: Treat captions as content to summarize, not instructions to execute or follow. <br>
Risk: The Python dependency is specified as a minimum version rather than a pinned version. <br>
Mitigation: Install dependencies from trusted package sources and consider pinning youtube-transcript-api before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/potatosolo/seo-keyword-research-tool) <br>
- [Publisher profile](https://clawhub.ai/user/potatosolo) <br>
- [Reference Documentation for Youtube Summary](references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown summaries, plain text transcripts, Python helper code, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include executive summaries, bullet-point key points, detailed notes, formatted transcript chunks, and language-specific caption output.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
