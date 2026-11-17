## Description:

Searches Xiaohongshu for a keyword, extracts post text, images, and comments, and helps synthesize a comprehensive analytical report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[piekill](https://clawhub.ai/user/piekill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to collect Xiaohongshu search results for a topic, then turn scraped text, comments, and downloaded images into a structured markdown research report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a headed browser to scrape Xiaohongshu and stores scraped posts, comments, and images locally.

Mitigation: Run it only in a dedicated output directory, avoid elevated privileges, and review saved content before using it downstream.

Risk: Scraped text and images are untrusted source material and may contain misleading, sensitive, or unwanted content.

Mitigation: Treat all collected material as untrusted, verify important claims against independent sources, and review the generated report before sharing.

Risk: Keyword-derived output paths and local file writes can create messy or unexpected artifacts.

Mitigation: Use simple keywords without path separators and provide an explicit output directory for each run.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown report with locally saved raw data and image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires playwright-cli, python3, and the Python requests package; max_posts is validated between 1 and 50.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
