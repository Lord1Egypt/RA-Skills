## Description:

Helps agents turn Xiaohongshu post links into shareable xhslink.com short links in batches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuiyunhai](https://clawhub.ai/user/cuiyunhai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents shorten Xiaohongshu post URLs for sharing or campaigns, including batches of up to 50 links through a paid service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default service address uses plaintext HTTP for authenticated requests, which could expose the account token and paid credits.

Mitigation: Use a trusted service and network, prefer a valid HTTPS address, avoid insecure TLS settings, and rotate any token that may have been exposed.

Risk: The supplied files describe keyword search rather than the URL shortener identified in the release listing.

Mitigation: Confirm the correct release files and pricing with the publisher before installing or running the skill.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cuiyunhai/skills/xhs-short-url)
- [ClawHub publisher profile](https://clawhub.ai/user/cuiyunhai)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Text guidance and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Short-link results and optional export; account credit may be charged per submitted link.]

## Skill Version(s):

2.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
