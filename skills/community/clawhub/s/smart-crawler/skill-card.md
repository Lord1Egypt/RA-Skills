## Description:

Smart Crawler helps agents collect web data with static and dynamic crawling, extraction rules, batch crawling, and anti-detection controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill for authorized web data collection, including static pages, dynamic pages, batch jobs, and structured extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad scraping, anti-detection behavior, unrestricted URL fetching, and unrestricted local output paths.

Mitigation: Use it only for authorized targets in an isolated, low-privilege environment with target allowlists, private-network blocking, redirect controls, and output writes constrained to a dedicated directory.

Risk: The dependency list uses broad version ranges.

Mitigation: Pin and review dependencies before production use.

Risk: Downloaded files and screenshots can be written to caller-provided paths.

Mitigation: Validate or normalize output paths and restrict them to approved working directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/smart-crawler)
- [Project homepage](https://github.com/openclaw/smart-crawler)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Crawler code can produce fetched HTML, extracted data, screenshots, downloads, JSON, CSV, Excel files, and database writes when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
