## Description:

Helps agents guide local Xiaohongshu note and comment collection, keyword search, and basic public-opinion analysis that requires a logged-in account or a paid API option.

This skill is for research and development only.

## Publisher:

[featherjiaxin-oss](https://clawhub.ai/user/featherjiaxin-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators use this skill to understand how to run Xiaohongshu crawling workflows for keyword search, comment collection, exported datasets, and lightweight engagement-based sentiment summaries. Users should review platform permissions and run the workflow only in an isolated local environment with an appropriate account or approved API provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may require account sessions and unreviewed third-party crawler code.

Mitigation: Use an isolated environment, a separate browser profile, and a dedicated low-privilege Xiaohongshu account where allowed; review and pin exact code and dependencies before execution.

Risk: Collected comments, IP region, author details, databases, and media can contain sensitive or personal data.

Mitigation: Restrict access to exported files, avoid shared token or session storage, and delete collected data when it is no longer needed.

Risk: Scraping Xiaohongshu may violate platform rules or create account enforcement risk if run too aggressively or without permission.

Mitigation: Confirm allowed use before crawling, keep request rates conservative, and prefer approved API access where available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/featherjiaxin-oss/skills/xhs-crawler)
- [ClawHub publisher profile](https://clawhub.ai/user/featherjiaxin-oss)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell command snippets and Python code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When a crawler is run locally, downstream artifacts may include Excel files, SQLite databases, and downloaded images or videos.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
