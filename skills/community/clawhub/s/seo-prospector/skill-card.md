## Description:

Automated SEO prospect research and outreach for web designers, agencies, and freelancers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrmooseyman](https://clawhub.ai/user/mrmooseyman)

### License/Terms of Use:

Proprietary

## Use Case:

External web designers, agencies, freelancers, and SEO consultants use this skill to research local business prospects, run SEO audits, generate prospect reports, draft outreach, and manage lead-pipeline status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill researches external websites and uses third-party APIs, which may share business, prospect, or query data outside the local workspace.

Mitigation: Review and approve external data sharing before use, configure API providers intentionally, and disclose third-party API usage to operators.

Risk: Generated prospect reports and outreach may be inaccurate, misleading, or inappropriate for privacy and anti-spam obligations.

Mitigation: Manually review every prospect report and outreach package for factual accuracy, consent, opt-out language, and applicable compliance requirements before sending.

Risk: URL auditing and verification can make network requests to arbitrary destinations, including unexpected or private-network targets.

Mitigation: Add destination allowlisting, block private-network ranges, and review target URLs before running audits in production.

Risk: Helper scripts store lead and outreach data locally in the user's OpenClaw workspace.

Mitigation: Treat generated lead data as sensitive, restrict filesystem access, and apply retention or deletion practices appropriate for the user's business.

Risk: API keys can be exposed through command arguments when invoking curl-based API calls.

Mitigation: Move API credentials to safer secret handling, avoid passing keys in process-visible arguments, and rotate exposed credentials.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/mrmooseyman/skills/seo-prospector)
- [Publisher Homepage](https://louisvillewebguy.com)
- [Support](https://github.com/hunterwilson/seo-prospector/issues)
- [Workflow Guide](artifact/references/workflow-guide.md)
- [Research Template](artifact/references/research-template.md)
- [Outreach Templates](artifact/references/outreach-templates.md)
- [Industry Insights](artifact/references/industry-insights.md)
- [Objection Handling](artifact/references/objection-handling.md)
- [Configuration Template](artifact/references/config-template.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown reports, outreach drafts, HTML email, JSON tracking records, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local prospect reports, outreach packages, daily summaries, and lead-pipeline state under the user's OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
