## Description:

Compares two to five YouTube channels by recent-video views, likes, comments, engagement rate, posting frequency, and a normalized trending score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcbaivn](https://clawhub.ai/user/mcbaivn)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and analysts use this skill to benchmark competing YouTube channels and generate a local comparison report from recent public video metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions download mutable remote files directly into the active skills folder without integrity checks.

Mitigation: Install the packaged reviewed files or pin and review an exact source revision before installing.

Risk: The script contacts YouTube through yt-dlp and writes comparison reports locally.

Mitigation: Run it with normal user privileges, review expected network access, and check the generated Youtube_Compare output before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcbaivn/skills/youtube-channel-compare)
- [ClawHub publisher profile](https://clawhub.ai/user/mcbaivn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Plain text comparison report with Markdown-style headings and metric rows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local Youtube_Compare report file and prints the report to stdout.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
