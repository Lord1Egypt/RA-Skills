## Description: <br>
Summarize YouTube videos with youtube2md, including bare YouTube URLs with no instructions, chaptered notes, timestamp links, transcript extraction, and key takeaways. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunghyo](https://clawhub.ai/user/sunghyo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and external users can use this skill to summarize one or more YouTube videos into structured Markdown notes, chapters, timestamp-aware takeaways, or transcript-only output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a pinned third-party youtube2md CLI and its dependency chain. <br>
Mitigation: Install only the reviewed pinned package version, prefer vetted internal mirrors in stricter environments, and re-audit dependencies before version bumps. <br>
Risk: Full mode can send transcript or audio-derived content to OpenAI APIs when OPENAI_API_KEY is provided. <br>
Mitigation: Do not set OPENAI_API_KEY for sensitive content; use simple or transcript mode when captions are available and external API use is not acceptable. <br>
Risk: YouTube cookie environment variables are credentials and may expose signed-in session context to the local tool runtime. <br>
Mitigation: Use cookies only when needed, keep them out of logs and commits, prefer short-lived exports, and delete them after sensitive runs. <br>
Risk: Generated summaries and transcripts may be saved locally. <br>
Mitigation: Use writable, controlled output directories and avoid publishing generated summaries or transcript artifacts inside release packages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunghyo/skills/youtube-summary) <br>
- [Output format](references/output-format.md) <br>
- [Security and installation considerations](references/security.md) <br>
- [youtube-summary behavior](references/summarization-behavior.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown summaries, transcript text, JSON transcript artifacts, and concise troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Full mode can use OpenAI APIs; simple and transcript modes use extracted captions or prepared transcript text when available.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
