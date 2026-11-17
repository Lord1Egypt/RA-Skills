## Description:

Xiaohongshu Skill helps an agent search Xiaohongshu content, inspect note details, generate topic reports, and publish user-provided notes through a local Windows Chromium browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ken0521](https://clawhub.ai/user/ken0521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to automate Xiaohongshu workflows on Windows, including content search, trend tracking, note-detail review, Markdown report generation, and interactive post publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores authenticated Xiaohongshu cookies and a persistent browser profile on the local machine.

Mitigation: Treat the stored cookies and browser profile like credentials; avoid shared or elevated machines and remove the profile when access is no longer needed.

Risk: The skill can publish content from the user's Xiaohongshu account.

Mitigation: Review all titles, body text, and image paths manually before allowing publish actions.

Risk: The setup flow installs Playwright and may use a third-party download mirror for Chromium.

Mitigation: Prefer a pinned dependency and lockfile setup, and avoid third-party mirrors unless they are explicitly trusted.

## Reference(s):

- [Setup Guide](references/setup.md)
- [Xiaohongshu Skill on ClawHub](https://clawhub.ai/ken0521/skills/xiaohongshu-win)
- [Publisher Profile](https://clawhub.ai/user/ken0521)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files]

**Output Format:** [CLI text output, JSON search-result files, and Markdown topic reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can also perform authenticated browser actions for interactive Xiaohongshu publishing.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
