## Description:

Research Daily Push is a compatibility skill for daily literature updates that retrieves recent arXiv papers for a research topic, generates structured Markdown summaries with relevance ratings, and supports scheduled delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and external users use this skill to monitor a research area, receive concise summaries of recent arXiv papers, and prepare daily paper-push reports. The release notes indicate the skill is retained for backward compatibility with the unified research entry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary flags review-worthy implementation risks around dependency installation, plaintext arXiv requests, and unescaped external report content.

Mitigation: Review before installing; prefer a version that uses HTTPS for arXiv, validates arXiv links, escapes Markdown output, and declares Python dependencies in a Python requirements file.

Risk: Scheduled delivery or push settings may share research topics, summaries, and destination identifiers with external services.

Mitigation: Enable the documented cron schedule or push destination variables only after confirming the intended recipients and data-sharing expectations.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jirboy/skills/research-daily-push)
- [arXiv API query endpoint used by the artifact](http://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with summary sections, paper tables, relevance scores, PDF links, and optional shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report is generated from a user-provided research topic and may be used manually or through a documented cron schedule.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
