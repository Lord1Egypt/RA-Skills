## Description:

Save a personal grocery product watchlist and check nearby supermarket deals automatically by radius.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukasosterheider](https://clawhub.ai/user/lukasosterheider)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to maintain a local grocery watchlist, configure location and radius, and run daily or weekly checks for nearby supermarket offers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local watchlist may include a home area and shopping preferences.

Mitigation: Use a coarse location when possible and review or delete /data/workspace/data/supermarkt-watchlist.json when it is no longer needed.

Risk: Scheduled offer checks may send product and location-based queries to external search or fetch services.

Mitigation: Create the cron job only when recurring checks are desired, and keep product and location entries limited to what is needed for the search.

## Reference(s):

- [Offer Check Template](artifact/references/check-template.md)
- [ClawHub Skill Page](https://clawhub.ai/lukasosterheider/skills/supermarket-offer-watcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON watchlist configuration, and concise alert summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local JSON watchlist at /data/workspace/data/supermarkt-watchlist.json.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
