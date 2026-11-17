## Description:

Search YouTube videos on any topic, extract English subtitles, and generate detailed summaries with key topics, quotes, and timestamps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dillera](https://clawhub.ai/user/dillera)

### License/Terms of Use:


## Use Case:

Developers, researchers, and external users use this skill to find YouTube videos on a topic, select one, download English subtitles, and receive a structured content summary without watching the full video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts YouTube and writes subtitle text to the local working directory.

Mitigation: Run it only in environments where outbound YouTube access and temporary local subtitle files are acceptable.

Risk: Unpinned dependencies such as yt-dlp and requests can change behavior over time.

Mitigation: Install dependencies in a dedicated virtual environment and pin versions for repeatable releases.

Risk: Some videos may lack English subtitles or may only provide auto-generated subtitles.

Mitigation: Treat summaries as subtitle-derived aids and verify important conclusions against the source video.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style text with command examples and optional JSON search data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include top video results, key topics, an extractive summary, timestamped notable moments, and short quotes when subtitles are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
