## Description:

Monitor brand sentiment, crypto opinions, and product perception across social media with automated tracking, alerts, and multi-entity dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to analyze public sentiment about brands, products, competitors, crypto assets, or topics across public web and social sources. It supports one-time sentiment checks, scheduled monitoring, alerting on meaningful negative shifts, and comparison reports across multiple entities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ongoing monitoring may continue to influence future sessions beyond a one-time sentiment check.

Mitigation: Require explicit user consent for scheduled monitoring, define clear schedule limits, and keep tracking records in the local sentiment-analysis folder.

Risk: Activation preferences may be saved into shared main memory while tracking data is described as local.

Mitigation: Confirm before writing cross-session preferences and distinguish shared activation preferences from local sentiment reports and alert history.

Risk: Search queries and public-post URL requests leave the user's machine.

Mitigation: Avoid private or personal terms in queries unless the user explicitly asks, and disclose that public web lookups are needed for fresh sentiment analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/sentiment-tracker)
- [Skill homepage](https://clawic.com/skills/sentiment-tracker)
- [Setup guide](artifact/setup.md)
- [Memory template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with optional shell commands and local Markdown configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local files under ~/sentiment-analysis/ for memory, tracked entities, reports, and alerts.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
