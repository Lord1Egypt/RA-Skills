## Description:

Create UGC-style vertical ads with the PopNow API: ad script with hook variants, an AI presenter or the user's own consenting presenter, talking-avatar video, product B-roll and a 9:16 cut for TikTok, Reels and Meta ads. Quotes every step in USD first. Use when the user wants a UGC ad, a spokesperson video, a product testimonial-style creative or ad variations to test.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyuminjo](https://clawhub.ai/user/kyuminjo)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers and creators use this skill to draft and produce short vertical product ads for social platforms, including hook variations, presenter clips, product B-roll, and editing suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference media URLs are shared with PopNow and generation providers, and host logs may retain input arguments.

Mitigation: Avoid sensitive material and use only media the user has rights to share.

Risk: Using a person's likeness or voice without consent, or presenting synthetic content as a real testimonial, can mislead viewers and violate rights or platform rules.

Mitigation: Use a fictional presenter or obtain documented consent, disclose synthetic presenters where required, and use only claims the user confirms are true.

Risk: Multi-step media generation incurs paid API charges.

Mitigation: Use a dedicated API key with model restrictions and spending caps, and review the quoted total before approving generation.

## Reference(s):

- [PopNow UGC Ads](https://popnow.ai/for/ugc-ads)
- [PopNow API task documentation](https://popnow.ai/docs/tasks)

## Skill Output:

**Output Type(s):** [Text, Images, Video, Guidance]

**Output Format:** [Markdown scripts and editing suggestions, with links to generated presenter images and video clips; optional assembled 9:16 MP4s.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically includes three hook variants and a shared 15–30 second body; generated media is returned as links.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
