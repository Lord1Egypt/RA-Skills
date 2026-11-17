## Description:

Extracts structured data from websites and APIs for analysis, including product prices, news articles, web-page datasets, and public-source research collections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research teams use this skill to collect structured data from permitted public websites or APIs and save it in formats suitable for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTPS certificate verification is disabled when fetching pages.

Mitigation: Remove the TLS verification bypass, or make insecure fetching an explicit opt-in that is off by default.

Risk: The scraper can fetch arbitrary internal, local, or private URLs from the agent environment.

Mitigation: Run it in a constrained network environment and restrict scraping to approved public targets.

Risk: Saved scrape outputs may contain sensitive or regulated data.

Mitigation: Avoid authenticated or sensitive targets and handle generated output files as potentially sensitive.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/skills/scraper-pro)
- [ClawHub Publisher Profile](https://clawhub.ai/user/dinghaibin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples, YAML configuration examples, and scraper outputs in JSON, CSV, or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write scraped output files to user-specified paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
