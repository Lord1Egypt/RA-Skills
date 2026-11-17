## Description:

Scrapes LinkedIn company people pages, filters target roles, ranks candidates with AI, and drafts personalized outreach plus a competitive team brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[behruamm](https://clawhub.ai/user/behruamm)

### License/Terms of Use:


## Use Case:

External recruiters, recruiting operations teams, and competitive intelligence users use this skill to collect authorized role-filtered LinkedIn people data, prioritize potential candidate targets, and prepare outreach materials and a talent brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a silent weekly auto-update path that can pull and reinstall mutable code.

Mitigation: Remove the auto-update block or require explicit user consent, and install the toolkit from a verified pinned version.

Risk: The workflow processes scraped personal profile data through external scraping and AI services.

Mitigation: Confirm authorization to collect and process the LinkedIn data, and confirm that sending it to the configured AI provider is permitted.

Risk: The skill requires API keys for scraping and AI providers.

Mitigation: Run in an isolated environment and avoid exposing credentials during installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/behruamm/skills/talent-scout)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with CLI commands; generated reports may be JSON or PDF.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIFY_API_KEY and one configured AI provider key.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
