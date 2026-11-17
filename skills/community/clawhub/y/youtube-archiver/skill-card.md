## Description:

Archive YouTube playlists into markdown notes with metadata, transcripts, AI summaries, and tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benmillerat](https://clawhub.ai/user/benmillerat)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to import and sync YouTube playlists into local markdown notes, then optionally enrich those notes with transcripts, AI summaries, and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access browser-authenticated YouTube data or a cookies.txt file.

Mitigation: Use dry runs first, provide only the cookies needed for the target playlists, and avoid sharing the output directory with untrusted users.

Risk: Transcript content may be sent to configured external AI providers for summaries or tags.

Mitigation: Review .config.json before enrichment, set providers to none when AI enrichment is not needed, and use least-privilege API keys stored in environment variables.

Risk: Custom base_url settings can route prompts and API keys to an untrusted endpoint.

Mitigation: Keep default provider endpoints unless the endpoint is fully trusted, and inspect any custom base_url values before running enrichment.

Risk: Playlist names and configured output paths influence where markdown files are written.

Mitigation: Choose a dedicated archive output directory and keep playlist names as simple folder labels without path characters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/benmillerat/skills/youtube-archiver)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Provider setup](references/providers.md)
- [Troubleshooting](references/troubleshooting.md)
- [Default summary prompt](references/default-summary-prompt.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown notes with YAML frontmatter, transcript sections, AI summaries, tags, and inline shell commands for setup or sync jobs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create local markdown files, .config.json, README.md, .sync-state.json, and a lockfile under the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
