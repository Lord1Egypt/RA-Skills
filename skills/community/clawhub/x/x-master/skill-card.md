## Description:

Master routing skill for X/Twitter operations, including reading tweets, searching discourse, researching trends, drafting posts, handling engagement, and routing direct API work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremyknows](https://clawhub.ai/user/jeremyknows)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to route X/Twitter work to the correct retrieval, research, posting, engagement, or API workflow while preserving manual approval for publishing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tweet retrieval may disclose requested X/Twitter URLs to the third-party fxtwitter proxy.

Mitigation: Avoid using fxtwitter for sensitive investigations unless that disclosure is acceptable; use official or trusted internal APIs where required.

Risk: Posting, replies, and engagement actions can publish public content from a configured account.

Mitigation: Keep posting in draft-only or manual approval mode and confirm the exact account and text before any publishing action.

Risk: Optional sub-skills and direct API workflows may require X OAuth or other service credentials.

Mitigation: Review and pin optional sub-skills before use, and expose credentials only to trusted, necessary workflows.

## Reference(s):

- [X Master on ClawHub](https://clawhub.ai/jeremyknows/skills/x-master)
- [The fxtwitter Pattern](references/fxtwitter-pattern.md)
- [Algorithm Intelligence](references/algo-intel.md)
- [FxTwitter](https://github.com/FixTweet/FxTwitter)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline JSON, JavaScript, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes tasks to optional sub-skills and requires manual approval before publishing to X/Twitter.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
