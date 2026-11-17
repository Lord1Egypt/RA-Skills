## Description:

Fetches current top trending topics on X (Twitter) for any country using public aggregators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anishtr4](https://clawhub.ai/user/anishtr4)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and external users use this skill to fetch current public X trending topics for a selected country or worldwide without an X account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trend data is fetched from public third-party web content and may be incomplete, inaccurate, or affected by upstream page changes.

Mitigation: Treat results as informational, verify important trends against authoritative sources, and monitor parser failures.

Risk: The reviewed artifact has dependency and runtime-hardening gaps called out by the security guidance.

Mitigation: Prefer pinned and synchronized dependencies, request timeouts, response-size limits, and terminal-output sanitization before automated or shared use.

## Reference(s):

- [getdaytrends.com](https://getdaytrends.com)
- [ClawHub skill page](https://clawhub.ai/anishtr4/skills/x-trends-dev)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Colorized terminal table or JSON array]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes rank, trend name, tweet volume when available, and source link.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and package metadata report 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
