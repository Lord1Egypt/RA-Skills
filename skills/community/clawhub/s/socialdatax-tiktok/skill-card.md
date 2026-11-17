## Description:

This skill retrieves TikTok videos, image posts, post details, comments, creator profiles, and creator post lists for research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, marketers, and social media analysts use the skill to search TikTok content and review posts, comments, and creator profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill repeatedly invokes an unpinned latest CLI package that could change and access configured credentials.

Mitigation: Wait for a reviewed, fixed CLI version before installation; when using the skill, provide only the credential and access needed for the requested data calls.

Risk: Search terms, links, or text submitted for analysis may be sent to SocialDataX.

Mitigation: Send only search terms, links, and text you are comfortable sharing with SocialDataX.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub release page](https://clawhub.ai/devinchen2014/skills/socialdatax-tiktok)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured TikTok data results with text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested TikTok search, post, comment, or creator lookup.]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
