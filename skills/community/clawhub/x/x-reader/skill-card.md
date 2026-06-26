## Description: <br>
X Reader fetches, transcribes, and analyzes content from URLs, files, or transcripts across supported web, social, video, RSS, and messaging platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lifecn](https://clawhub.ai/user/lifecn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agent users use X Reader to turn web pages, posts, feeds, videos, and transcripts into structured content, summaries, and action-oriented analysis. It is useful when an agent needs to fetch source material, preserve useful excerpts, or produce concise takeaways from multi-platform content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URLs, fetched content, and sometimes audio may be sent to third-party services such as Jina, Groq, Telegram, and platform APIs. <br>
Mitigation: Use only approved public URLs, avoid private or internal links, and configure service credentials only for accounts intended for this workflow. <br>
Risk: Fetched content can be retained locally in a JSON inbox or optional Markdown archive. <br>
Mitigation: Leave OUTPUT_DIR and OBSIDIAN_VAULT unset when archives are not needed, and store any configured inbox or vault in an approved location. <br>
Risk: Authenticated browser or Telegram sessions may reuse user-created platform logins. <br>
Mitigation: Avoid saved logins when authenticated scraping is not intended, protect session files, and rotate or revoke credentials if a session is no longer trusted. <br>
Risk: The MCP server can expose content-reading tools if configured for network transport. <br>
Mitigation: Prefer stdio or localhost use; require authentication and a trusted reverse proxy before exposing the server beyond the local machine. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lifecn/x-reader) <br>
- [Publisher profile](https://clawhub.ai/user/lifecn) <br>
- [Groq API keys](https://console.groq.com/keys) <br>
- [Telegram API credentials](https://my.telegram.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and analysis, JSON content records, and shell or configuration snippets when setup is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save fetched content to a JSON inbox and optional Markdown archive when configured; transcript completeness depends on available subtitles or transcription services.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata, pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
