## Description:

Searches Xiaohongshu (小红书) for a keyword, extracts posts with text, images, and comments, and helps synthesize the results into a concise analytical report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seckho1985](https://clawhub.ai/user/seckho1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to collect Xiaohongshu search results for a topic and convert posts, comments, and images into a thematic Markdown summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches a headed browser and may require Xiaohongshu login during scraping.

Mitigation: Run it in a disposable browser/workspace and avoid exposing unrelated authenticated sessions or sensitive data.

Risk: The skill runs mutable external Playwright tooling.

Mitigation: Pin and review Playwright dependencies before execution.

Risk: The skill saves scraped posts, comments, and images locally and may write outside the intended output path under some inputs.

Mitigation: Use a non-sensitive output directory and avoid path-like keywords or inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seckho1985/skills/xhs-search-summarizer-seckho)
- [Publisher profile](https://clawhub.ai/user/seckho1985)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown report with local image files and supporting scrape output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create raw data Markdown, JSON scrape output, and downloaded image files in the selected output directory.]

## Skill Version(s):

1.0.3 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
