## Description:

A read-only Xiaohongshu (Rednote) trend research skill that returns structured JSON for note search, note details, comments, and creator posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and analysts use the skill to search public Xiaohongshu notes, inspect note details and comments, and review creator posts and audience metrics for trend research, competitor monitoring, KOL screening, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports privacy and permission-scope concerns, including a confirmed support-sharing concern and an unresolved third-party data notice.

Mitigation: Review the provider's data notice and avoid sending sensitive queries or links; use public data for internal analysis.

Risk: ClawScan analysis of some executable files was incomplete, so the scan does not establish that the skill is safe.

Mitigation: Review and scan the release before enabling it, and keep the API token out of prompts and logs.

## Reference(s):

- [Usage and safety instructions](SKILL.md)
- [Output contract](references/contract.md)
- [Command options](references/options.md)
- [Intent routing](references/routing.md)
- [Error handling](references/errors.md)
- [Provider website](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/guaikei/skills/xhs-trend)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public note, comment, creator, and engagement data; request limits vary by plan.]

## Skill Version(s):

1.2.3 (source: server-resolved release metadata, SKILL.md frontmatter, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
