## Description:

Scrape documentation content from Zoomin Software portals using Playwright browser automation to handle dynamic content loading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[recklessop](https://clawhub.ai/user/recklessop)

### License/Terms of Use:


## Use Case:

Developers and documentation engineers use this skill to scrape rendered article text from Zoomin-powered documentation portals when standard static fetching does not capture the main content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The URL list can drive a browser to arbitrary addresses.

Mitigation: Install only when the URL source is trusted, avoid URLs containing secrets, and restrict or validate URLs to expected Zoomin documentation domains before running.

Risk: The scraper writes extracted content to a local output directory.

Mitigation: Run in a constrained environment with a dedicated virtual environment and choose an output directory that can be safely populated.

Risk: The release security verdict is suspicious and requires review before installation.

Mitigation: Review the skill and scan results before deployment, and constrain network and filesystem access during execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/recklessop/skills/zoomin-scraper-recklessop)

## Skill Output:

**Output Type(s):** [Text, Files, JSON, Shell commands, Guidance]

**Output Format:** [Extracted documentation text files, JSON batch-analysis summaries, and Markdown usage guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a URL list, output directory, Python virtual environment, Playwright, and Chromium browser binaries.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
