## Description:

Skill Recommender Pro recommends OpenClaw skills by analyzing installed skill names with rule-based filtering and pattern matching, then suggesting complementary skills, alternatives, and gap-fillers in multiple languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to review installed skills, identify gaps, and receive complementary, alternative, and popular skill recommendations with install suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect installed skill names and query public ClawHub metadata to generate recommendations.

Mitigation: Use it where installed skill names can be shared for recommendation purposes, and avoid supplying secrets or private configuration data.

Risk: Recommendation reports may include suggested install commands for additional skills.

Mitigation: Review each recommended skill and its rationale before running install commands.

Risk: Recommendations depend on available ClawHub metadata and may be incomplete or stale.

Mitigation: Treat the report as decision support and verify current skill details before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tobewin/skills/skill-recommender-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports with optional inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output language follows the user's conversation language or requested language.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
