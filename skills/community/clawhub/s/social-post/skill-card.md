## Description:

Post and reply to X/Twitter and Farcaster with text and images, including multi-account support, draft preview, character validation, threads, replies, image uploads, and documented platform costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[callmedas69](https://clawhub.ai/user/callmedas69)

### License/Terms of Use:

MIT

## Use Case:

External creators, developers, and social operators use this skill to preview, validate, and publish posts or replies across X/Twitter and Farcaster, including images, threads, link shortening, and platform-specific limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public posts or replies and spend Farcaster wallet funds.

Mitigation: Use dry-run previews first, require explicit approval for real posting, keep only minimal funds in the Farcaster wallet, and use dedicated low-privilege social accounts.

Risk: Secrets and credentials are handled through local files and mutable external code paths.

Mitigation: Review scripts before installation, restrict credential file permissions, avoid sensitive images or token-bearing URLs, and revise the package to parse secrets safely and pin external executable dependencies before broad use.

Risk: Anti-spam bypass positioning can create platform policy or reputational risk.

Mitigation: Use variation features only for legitimate account-specific wording, review platform policies, and remove bypass-oriented positioning before wider deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/callmedas69/skills/social-post)
- [X Developer Portal](https://developer.twitter.com/en/portal/dashboard)
- [X API pricing](https://developer.twitter.com/#pricing)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell command examples and plain-text posting output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can trigger public social posts, replies, image uploads, and Farcaster wallet spending when run outside dry-run mode.]

## Skill Version(s):

1.4.0 (source: frontmatter, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
