## Description:

Automates Twitter/X growth and content workflows for AI and Tech Twitter, including trend discovery, tweet drafting, posting, follow-back engagement, and quote-tweet preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and operators managing AI or Tech Twitter accounts use this skill to discover current AI topics, draft English-language tweets, publish or prepare posts, and run follow-back or quote-tweet engagement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or prepare posts from a user's Twitter/X account through automated workflows.

Mitigation: Use only with an account intended for ZeeLin or AI promotional automation and require manual review of every final tweet before posting.

Risk: The artifact calls hard-coded local publisher paths that are not bundled with this release.

Mitigation: Replace external publisher paths with a bundled or integrity-checked implementation before use.

Risk: Noninteractive posting and growth engagement can create unwanted account activity.

Mitigation: Avoid unattended auto-posting on valued accounts and keep engagement activity within explicit, reviewed limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kelcey2023/skills/zeelin-twitter-x-auto-ops)
- [X](https://x.com)
- [Hacker News Algolia API](https://hn.algolia.com/api/v1/search?query=AI&tags=story&hitsPerPage=5)
- [THU ZeeLin Reports](https://thu-nmrc.github.io/THU-ZeeLin-Reports/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with tweet text, operational guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some workflows open X pages, fetch public trend or report data, or call local posting helpers when executed.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
