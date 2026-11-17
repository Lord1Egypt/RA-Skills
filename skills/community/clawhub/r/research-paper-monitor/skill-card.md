## Description:

Monitors academic papers for user-selected keywords, generates Chinese summaries and local Markdown reports, with live arXiv support and optional notification workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wiltonmotta](https://clawhub.ai/user/wiltonmotta)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, graduate students, teachers, and research teams use this skill to configure keyword-based literature monitoring, archive matching papers, and generate Chinese daily or weekly digests for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence says the skill overstates some capabilities and several listed data sources are incomplete or dependent on external access.

Mitigation: Verify each enabled source in a test run before relying on it; treat non-arXiv sources as requiring review or completion unless local testing proves otherwise.

Risk: Webhook URLs, research interests, user profile fields, and paper metadata may be stored locally or sent to external services when optional integrations are enabled.

Mitigation: Protect ~/.openclaw/research-monitor/config.json with owner-only permissions, rotate any real webhook copied from documentation, and enable Feishu, email, Zotero, cron, or backup integrations only after reviewing data-sharing expectations.

Risk: The security guidance calls out arXiv access over HTTP.

Mitigation: Change arXiv API access to HTTPS before production use.

## Reference(s):

- [Detailed Configuration](references/configuration.md)
- [Academic Data Sources](references/data-sources.md)
- [Advanced Usage](references/advanced-usage.md)
- [arXiv](https://arxiv.org/)
- [arXiv API](http://export.arxiv.org/api/)
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/)
- [Google Scholar](https://scholar.google.com/)
- [CNKI](https://www.cnki.net/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON configuration and index files, Python command lines, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local paper archives and digest reports under configured paths, with optional outbound notification payloads when enabled.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
