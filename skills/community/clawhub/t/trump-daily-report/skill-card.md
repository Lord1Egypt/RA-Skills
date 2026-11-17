## Description:

Tracks Trump social posts and major U.S. media coverage to produce bilingual market analysis reports for morning and evening briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xsqorange](https://clawhub.ai/user/xsqorange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to have an agent gather public Trump-related social, news, and market signals, compare them with recent report history, and produce bilingual market briefings. The workflow supports English and Chinese report generation, local report archiving, and configured Feishu delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches public news and market data from named external sources, including r.jina.ai as a fallback proxy.

Mitigation: Install only if those external data sources and fallback proxy use are acceptable for the deployment environment.

Risk: Generated reports are retained under the configured memory_path.

Mitigation: Set memory_path to an approved location and apply the organization's retention and access controls to saved reports.

Risk: The workflow can post English and Chinese reports to a configured Feishu group.

Mitigation: Verify the Feishu group configuration before use and restrict delivery to intended recipients.

## Reference(s):

- [Trump Daily Report Skill Page](https://clawhub.ai/xsqorange/skills/trump-daily-report)
- [Media Sources](references/media-sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Bilingual Markdown reports, saved Markdown files, Feishu messages, and shell/Python command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains report history under the configured memory_path and can post English and Chinese reports to a configured Feishu group.]

## Skill Version(s):

1.2.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
