## Description:

Tracks and compares competitor follower growth across Twitter/X, TikTok, and Instagram using apidojo scrapers on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Competitive intelligence analysts, marketing teams, CMOs, and growth strategists use this skill to compare competitor follower counts, engagement benchmarks, and growth indicators across social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Competitor lists, monitored accounts, and Apify usage may reveal sensitive business plans.

Mitigation: Review account lists before use, limit access to outputs, and avoid running the skill for confidential launches or campaigns without approval.

Risk: API-token examples that pass tokens in query parameters can expose credentials through logs, shell history, or shared URLs.

Mitigation: Use a least-privilege APIFY_TOKEN stored in the environment and prefer Authorization headers or managed tool credentials.

Risk: Follower-list, following-list, retweeter extraction, and custom JavaScript transformations can broaden data collection beyond simple account benchmarking.

Mitigation: Keep expanded extraction disabled unless required and review any custom transformation before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/tracking-competitor-social-media-growth)
- [API Dojo publisher profile](https://clawhub.ai/user/apidojo-io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with comparison tables and inline shell or API commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save Apify actor results as CSV or JSON when the user asks for files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
