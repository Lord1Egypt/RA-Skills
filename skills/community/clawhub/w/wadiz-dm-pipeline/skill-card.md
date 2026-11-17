## Description:

Automates local Wadiz crowdfunding project crawling, filters projects with 50-99% funding, analyzes project pages, and generates personalized outreach DMs for makers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thedalbee](https://clawhub.ai/user/thedalbee)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers and operators use this skill to collect Wadiz crowdfunding prospects, generate personalized Korean DM copy, and export reviewable outreach CSV files for manual use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local browser crawler against Wadiz and may create traffic that is blocked or inappropriate for the target site.

Mitigation: Run it locally as documented, keep request volumes low, preserve the built-in delay, and follow the target site's terms and outreach policies.

Risk: When ANTHROPIC_API_KEY is configured, scraped project title and description text is sent to Anthropic for DM generation.

Mitigation: Review what data will be processed before enabling the key, avoid sensitive project content, or run without the key to use the local template fallback.

Risk: Generated outreach DMs may be inaccurate, unsuitable, or noncompliant if sent without review.

Mitigation: Treat the CSV as a draft queue and manually review, edit, and approve messages before any outreach.

Risk: The skill text mentions Tumblbug, but security evidence says to expect Wadiz support only.

Mitigation: Use the release for Wadiz workflows unless the publisher adds Tumblbug support evidence and tests.

## Reference(s):

- [DM template](references/dm-template.md)
- [Wadiz rewards](https://www.wadiz.kr/web/wreward/main?sort=funding&status=opening)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; generated pipeline output is CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The pipeline writes dm_results_YYYYMMDD_HHMM.csv under output/ when run.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
