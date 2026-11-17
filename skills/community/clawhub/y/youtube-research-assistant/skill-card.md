## Description:

Fetch transcripts from YouTube videos to provide structured multilingual summaries, Q&A, and deep dives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maheshmuke](https://clawhub.ai/user/maheshmuke)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch YouTube captions with yt-dlp, store local transcript files, and generate transcript-grounded summaries, Q&A responses, deep dives, and action points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports under-scoped network access and recommends review before installation.

Mitigation: Use the skill only in a contained environment until network behavior is narrowed to the intended YouTube subtitle fetch path.

Risk: The security guidance flags URL and video ID validation gaps.

Mitigation: Validate YouTube URLs and video IDs before invoking transcript fetch commands.

Risk: The security guidance flags use of --no-check-certificates.

Mitigation: Remove --no-check-certificates so yt-dlp uses normal certificate validation.

Risk: The security review warns against use with sensitive local text files or private network access available to OpenClaw.

Mitigation: Run the skill where it cannot access sensitive local files or private network resources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maheshmuke/skills/youtube-research-assistant)
- [ClawHub publisher profile](https://clawhub.ai/user/maheshmuke)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown-style text with timestamped transcript excerpts and local transcript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python 3 and yt-dlp; transcript files, session state, and index data are stored locally and old transcripts are cleaned after 24 hours.]

## Skill Version(s):

5.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
