## Description:

This skill automates Xiaohongshu login, content publishing, search, browsing, and social interactions through Chrome DevTools Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinadu-ai](https://clawhub.ai/user/tinadu-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to manage a logged-in Xiaohongshu account for publishing image posts, videos, and long articles; searching and reading content; and performing comments, likes, and favorites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a real logged-in Xiaohongshu account and may post, comment, like, favorite, scrape page data, and retain browser session state locally.

Mitigation: Use a dedicated account, review commands and content before execution, and avoid running the skill on machines that contain sensitive data.

Risk: The security review notes weakened browser protections and limited safeguards around session data.

Mitigation: Run Chrome under a dedicated non-root user in an isolated environment, and review the no-sandbox browser behavior before use.

Risk: Untrusted image URLs or CLI arguments can increase operational and account risk.

Mitigation: Use trusted image sources and validated CLI inputs only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tinadu-ai/skills/xiaohongshu-v2)
- [Publisher profile](https://clawhub.ai/user/tinadu-ai)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [JSON command results, local files such as login QR codes, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10+, Chrome 120+, and access to a logged-in Xiaohongshu account.]

## Skill Version(s):

2.0.0 (source: skill.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
