## Description:

Provides read-only access to public Xiaohongshu (Rednote) search results, note details, comments, creator posts, and account engagement data as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, analysts, and developers use it to compare public Rednote posts and accounts, monitor comment sentiment, and research content topics from structured results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends search terms or public content links to the third-party API; ClawScan also reports concerns about data-sharing disclosures.

Mitigation: Review the provider's data-handling terms and avoid sending sensitive search terms or links.

Risk: ClawScan reports partial inspection and missing tool-scope declarations, and says its evidence does not establish that the skill is safe.

Mitigation: Review the uninspected components and tool permissions before installation; follow the scanner guidance if those concerns are not acceptable.

## Reference(s):

- [Guaikei API service](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/guaikei/skills/xhs-rival)
- [Output contract](references/contract.md)
- [Command options](references/options.md)
- [Error handling](references/errors.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Structured JSON result envelope with command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results cover public searches, notes, comments, and creator profiles; available counts depend on the requested plan and limits.]

## Skill Version(s):

1.2.3 (source: release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
