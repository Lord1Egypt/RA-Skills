## Description:

Extracts clean plain-text or JSON transcripts from existing YouTube captions using native Node.js and a local yt-dlp binary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jwestburg](https://clawhub.ai/user/jwestburg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to fetch existing captions from a supported single-video YouTube URL and hand clean transcript text to summarization, quote extraction, research triage, or downstream tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full YouTube URLs may contain tracking, tokens, or other sensitive query parameters and are sent to YouTube through yt-dlp.

Mitigation: Avoid private or client-sensitive videos and strip tracking, token, or other sensitive query parameters before use or downstream logging.

Risk: Normal operation depends on a trusted local yt-dlp binary that contacts YouTube for the supplied video.

Mitigation: Use a trusted yt-dlp binary on PATH, keep the wrapper's YouTube-only single-video allowlist, and do not install or update yt-dlp through the skill without explicit approval.

Risk: Video titles and transcript text are untrusted third-party content and may be inaccurate, auto-generated, copyrighted, or adversarial to downstream agents.

Mitigation: Treat captions as data rather than instructions, summarize before quoting large passages, and republish long transcripts only when rights or permission are clear.

## Reference(s):

- [YouTube Transcript Contract](artifact/references/youtube-transcript-contract.md)
- [ClawHub skill page](https://clawhub.ai/jwestburg/skills/youtube-transcript-native-node)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON transcript output, with compact Markdown status and caveats from the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source URL, requested language, timestamp mode, auto-caption status, transcript status, caveats, next safe step, and saved path when file output is explicitly approved.]

## Skill Version(s):

1.1.27 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
