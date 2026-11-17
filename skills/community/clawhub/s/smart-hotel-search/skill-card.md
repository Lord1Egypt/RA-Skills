## Description:

Smart Hotel Search helps agents handle non-standard hotel requests by searching Xiaohongshu reviews, extracting candidate hotel names, and checking booking details through Fliggy via flyai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sgw153759-oss](https://clawhub.ai/user/sgw153759-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to turn scenario-based hotel preferences, such as pet-friendly stays, quiet rooms, or photo-friendly pools, into candidate hotel recommendations with user review context and booking information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install unpinned third-party command-line tools and a browser extension.

Mitigation: Verify the npm packages and extension source before installation, and install only in environments approved for travel-search automation.

Risk: The skill relies on an authenticated Chrome session for Xiaohongshu access.

Mitigation: Use a dedicated Chrome profile or test account, and avoid keeping unrelated sessions or sensitive data in that browser profile.

Risk: Hotel queries and preferences may be sent to Xiaohongshu, Fliggy, and related tooling.

Mitigation: Avoid entering sensitive personal information, and disclose that recommendations depend on third-party platforms and their data handling.

## Reference(s):

- [Smart Hotel Search on ClawHub](https://clawhub.ai/sgw153759-oss/skills/smart-hotel-search)
- [Installation guide](references/installation.md)
- [Examples](references/examples.md)
- [OpenCLI GitHub](https://github.com/jackwener/opencli)
- [OpenCLI npm package](https://www.npmjs.com/package/@jackwener/opencli)
- [flyai](https://open.fly.ai/)
- [flyai-cli npm package](https://www.npmjs.com/package/@fly-ai/flyai-cli)
- [Xiaohongshu](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and booking/review summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include hotel names, review excerpts or summaries, prices, scores, and booking links when the external tools return them.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
