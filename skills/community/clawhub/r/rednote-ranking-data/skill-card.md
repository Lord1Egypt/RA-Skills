## Description:

This skill helps users track daily, weekly, and monthly follower-growth rankings for RedNote accounts across fixed categories, generate ranking images, export Excel files, and manage report subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, MCN operators, brand teams, and content creators use this skill to monitor RedNote account growth trends, create shareable ranking visuals, export data for analysis, and receive scheduled ranking reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subscription delivery handles email addresses, WeChat identifiers, and delivery configuration with weak safeguards.

Mitigation: Protect subscription and configuration files, avoid real contact identifiers until storage is reviewed, and restrict access to generated delivery artifacts.

Risk: Ranking data is fetched over unauthenticated TLS, which can reduce confidence in the transport path.

Mitigation: Review and fix TLS certificate and hostname verification before relying on production data or running the skill on untrusted networks.

Risk: Generated Excel and email reports may include untrusted ranking content.

Mitigation: Treat exported spreadsheets and HTML reports as untrusted until spreadsheet escaping and HTML escaping are reviewed and fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/rednote-ranking-data)
- [Paid subscription tier design](artifact/references/subscription_tiers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with command examples; JSON ranking data, PNG ranking images, Excel spreadsheets, HTML email content, and WeChat template payloads when scripts are run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected category, ranking period, date, row limit, subscription settings, and delivery channel.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
