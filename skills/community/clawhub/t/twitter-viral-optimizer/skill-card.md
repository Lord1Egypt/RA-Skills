## Description:

Optimizes social media text for Twitter/X, Weibo, Xiaohongshu, and Douyin-style image posts by rewriting drafts, scoring algorithm fit, planning timing, suggesting hashtags, and producing A/B test guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External social media operators, product marketers, creators, and developers use this skill to turn draft posts into platform-specific rewrites, posting calendars, hashtag strategies, scoring tables, and post-publication improvement guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution even though its core behavior is social media content guidance.

Mitigation: Install or run it only where command execution is disabled, sandboxed, or tightly controlled.

Risk: Optional platform API features may require credentials.

Mitigation: Provide API keys only through environment variables and only when a specific API-backed workflow is needed.

Risk: Generated optimization advice could encourage platform-policy-sensitive or misleading content if used without review.

Mitigation: Review outputs before publishing and reject content involving misinformation, political or controversial topics, artificial engagement, or other platform policy violations.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with rewritten post variants, scorecards, timing tables, hashtag recommendations, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include multiple content variants, A/B testing plans, posting calendars, and risk notes for platform policy-sensitive content.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
