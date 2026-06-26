## Description: <br>
Archive YouTube playlists into markdown notes with metadata, transcripts, AI summaries, and tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benmillerat](https://clawhub.ai/user/benmillerat) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, knowledge workers, and external users use this skill to archive YouTube playlists such as Liked Videos and Watch Later into local markdown notes, then optionally enrich those notes with transcripts, summaries, and tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTube session cookies or an exported cookies file may grant playlist access beyond public videos. <br>
Mitigation: Use dry-run first, grant browser or cookies-file access only for the playlists you intend to archive, and keep any cookies file stored outside shared directories. <br>
Risk: Transcript and metadata content may be sent to remote AI providers when summaries or LLM tagging are enabled. <br>
Mitigation: Set summary and tagging providers to none or Ollama when content should stay local, or review the configured provider and API key environment variables before enrichment. <br>
Risk: Automated recurring imports can repeatedly read private playlist data and write new local notes. <br>
Mitigation: Add cron only after a successful manual run and review the exact import and enrichment commands, output directory, and batch limit. <br>


## Reference(s): <br>
- [Provider setup](references/providers.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Default summary prompt](references/default-summary-prompt.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Files] <br>
**Output Format:** [Markdown guidance with shell commands; generated markdown notes, JSON configuration, and sync state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run import and bounded enrichment batches; can run without remote AI providers by setting providers to none.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
