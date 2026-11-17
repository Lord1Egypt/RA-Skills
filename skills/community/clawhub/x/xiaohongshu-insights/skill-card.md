## Description:

Helps creators and marketers analyze publicly available Xiaohongshu posts, comments, and creator activity for competitor and content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, brand marketers, and content analysts use public Xiaohongshu search results, post details, comments, and creator activity to research trends, competitors, and audience responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, Xiaohongshu links, and the API token are sent to guaikei.com.

Mitigation: Avoid sensitive investigations unless this third-party data flow is acceptable; safeguard the API token.

Risk: Successful query results remain in local temporary storage.

Mitigation: Review and remove stored results according to your retention requirements.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/why20261/skills/xiaohongshu-insights)
- [Project homepage listed in release metadata](https://github.com/um-why/xiaohongshu-openclaw-skill)
- [API token and service information](https://www.guaikei.com)
- [Options and usage](references/options.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Shell commands]

**Output Format:** [Markdown guidance and structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful results are also saved locally under the system temporary directory.]

## Skill Version(s):

1.1.4 (source: release metadata, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
