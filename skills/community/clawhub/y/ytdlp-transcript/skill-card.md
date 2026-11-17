## Description:

Fetch and summarize transcripts from any YouTube video using yt-dlp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nerikko](https://clawhub.ai/user/nerikko)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch YouTube captions, convert them into readable transcript text, and ask an agent to summarize, translate, or extract insights from the video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency hygiene issues may cause stale or unnecessary package exposure.

Mitigation: Regenerate the lockfile from package.json, remove unused dependencies, and keep yt-dlp updated before installation.

Risk: The skill contacts YouTube for the supplied video and returns raw transcript text to the agent.

Mitigation: Use only videos appropriate for the workflow, and review transcript content before relying on summaries, translations, or extracted insights.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nerikko/skills/ytdlp-transcript)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text transcript with a language header]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires yt-dlp and Node.js 18+. The script fetches captions for a supplied YouTube URL or video ID, defaults to Portuguese, falls back to English, and outputs cleaned transcript text for the agent.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
