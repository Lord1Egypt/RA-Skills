## Description:

Use xiaohongshu-cli for Xiaohongshu operations including searching notes, reading content, browsing users, liking, collecting, commenting, following, and posting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackwener](https://clawhub.ai/user/jackwener)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate the xiaohongshu-cli tool for Xiaohongshu reading, discovery, account interaction, and creator workflows. It is intended for authenticated CLI use with local browser cookies and structured YAML or JSON output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use local browser-session cookies and perform authenticated Xiaohongshu actions.

Mitigation: Use a dedicated browser profile or test account, avoid sharing raw cookie values, and clear cached cookies with xhs logout when finished.

Risk: Mutating commands can like, collect, comment, follow, post, or delete account content.

Mitigation: Review every mutating command before execution and require explicit user confirmation for account-changing actions.

Risk: Aggressive or parallel requests may trigger captcha, rate limits, or IP blocks.

Mitigation: Do not parallelize requests; respect built-in delays and pause for browser captcha completion when verification is required.

Risk: Integration tests and real API workflows may contact Xiaohongshu with live credentials.

Mitigation: Do not run integration tests casually; run only in an intentional test environment with credentials suitable for that purpose.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackwener/skills/xiaohongshu-cli)
- [README](README.md)
- [Structured Output Schema](SCHEMA.md)
- [PyPI package](https://pypi.org/project/xiaohongshu-cli/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI results are YAML or JSON envelopes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local browser-cookie authentication and may trigger authenticated account actions.]

## Skill Version(s):

0.2.1 (source: ClawHub release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
