## Description:

Automates extraction of research paper metadata from shitjournal.org and supports AI-assisted abstract analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[excalibur9527](https://clawhub.ai/user/excalibur9527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers can use this skill to scrape article titles, abstracts, DOI values, and publication information from shitjournal.org for downstream review or knowledge workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on npm browser automation dependencies that may change over time.

Mitigation: Review and pin npm dependencies with a lockfile before installing or deploying the skill.

Risk: Future LLM-analysis behavior may send scraped abstracts to a model provider.

Mitigation: Confirm model-provider configuration and data handling expectations before enabling LLM analysis.

## Reference(s):

- [Skill release page](https://clawhub.ai/excalibur9527/skills/shit-journal-scraper)
- [shitjournal.org](https://shitjournal.org)

## Skill Output:

**Output Type(s):** [text, JSON, code, shell commands, guidance]

**Output Format:** [Markdown guidance and console text, with scraped article records suitable for JSON workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses browser automation to render the target site before extracting article metadata.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
