## Description:

Summarize YouTube videos with youtube2md, including bare YouTube URLs with no instructions, chaptered notes, timestamp links, transcript extraction, and key takeaways.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunghyo](https://clawhub.ai/user/sunghyo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn YouTube URLs into Markdown summaries, chaptered notes, key takeaways, or transcript outputs. It is useful when an agent needs concise video understanding while preserving timestamped source structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full mode can send transcript text or captionless-video audio-derived content to OpenAI.

Mitigation: Use simple or transcript mode for sensitive videos, or set YOUTUBE2MD_CAPTIONS_ONLY=1 so captionless videos fail instead of using audio transcription.

Risk: YouTube cookie file or raw cookie header settings can expose signed-in session credentials to the local tool runtime.

Mitigation: Prefer a short-lived cookie file over a raw cookie header, keep cookie values out of chats and logs, and remove them after use in sensitive environments.

Risk: Trust depends on the installed npm package and its dependency tree.

Mitigation: Install the pinned youtube2md@1.2.0 package from a vetted source, prefer unprivileged installs on shared systems, and re-audit before version bumps.

## Reference(s):

- [youtube2md README](https://github.com/sunghyo/youtube2md#readme)
- [ClawHub skill page](https://clawhub.ai/sunghyo/skills/youtube-summary)
- [Output format](artifact/references/output-format.md)
- [Security and installation considerations](artifact/references/security.md)
- [Summarization behavior](artifact/references/summarization-behavior.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, timestamped text or JSON transcripts, and setup or troubleshooting commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full mode passes through youtube2md Markdown; simple mode summarizes from timestamped transcript text; transcript mode returns transcript content.]

## Skill Version(s):

1.0.13 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
