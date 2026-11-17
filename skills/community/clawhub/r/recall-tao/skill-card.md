## Description:

桃噗噗回复助手 helps agents monitor Douyin Creator Center comments, classify and filter them, and draft or post compliant replies through browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hexiuqian](https://clawhub.ai/user/hexiuqian)

### License/Terms of Use:

MIT-0

## Use Case:

External Douyin account operators and their agents use this skill to monitor creator comments, apply keyword and sensitive-word rules, generate replies, and manage public reply workflows across videos and accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can act from an authenticated Douyin account and post public replies.

Mitigation: Prefer manual review or draft mode and approve reply text before posting.

Risk: Browser settings include sandbox-disabling and anti-detection flags while login state may be persisted.

Mitigation: Remove sandbox-disabling and anti-detection flags, and protect or disable persisted login state.

Risk: AI-generated reply text may be placed into executable browser JavaScript.

Mitigation: Treat generated replies as data, sanitize or escape them, and avoid direct interpolation into evaluate scripts.

Risk: Browser automation may navigate beyond the intended account workflow.

Mitigation: Restrict navigation to Douyin Creator Center URLs required for comment and content management.

## Reference(s):

- [Douyin Auto Reply Monitoring Guide](artifact/references/monitoring_guide.md)
- [Douyin Creator Center Comment Management](https://creator.douyin.com/creator-micro/interactive/comment)
- [Douyin Creator Center Content Management](https://creator.douyin.com/creator-micro/content/manage)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline browser commands, JavaScript snippets, JSON configuration, and generated reply text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May operate from an authenticated Douyin account; use review controls before public posting.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
