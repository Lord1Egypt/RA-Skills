## Description:

Provides SocialDataX tools for Xiaohongshu (XHS/RedNote) trend searches, note discovery and details, comment analysis, and creator lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to retrieve and summarize Xiaohongshu trends, posts, comments, and creator activity through SocialDataX.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious with medium confidence, citing a CLI package on a mutable latest version and automatic installation approval.

Mitigation: Consider avoiding installation until the CLI dependency is pinned to a reviewed version and its updates are checked.

Risk: Authentication uses a local credential file, and supplied search terms or URLs may be sent to SocialDataX.

Mitigation: Protect the local credential file and use only search terms and URLs appropriate to send to SocialDataX.

## Reference(s):

- [SocialDataX AI access and skill information](https://socialdatax.com/ai?from=clawhub)
- [ClawHub release page](https://clawhub.ai/devinchen2014/skills/socialdatax-xhs)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Structured data with concise Markdown summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search, note, comment, and creator results depend on the SocialDataX API response.]

## Skill Version(s):

0.1.28 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
