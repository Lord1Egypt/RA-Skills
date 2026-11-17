## Description:

Facebook Publisher Skill (Automate Page Posts via Graph API)

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunneetoichoi](https://clawhub.ai/user/yunneetoichoi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure Facebook Page publishing workflows, exchange Page tokens, publish text or image posts, schedule Page content, and test Graph API connectivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful Facebook user and Page access tokens and may print or save token values during helper flows.

Mitigation: Store tokens in protected environment variables or a secret manager, avoid logging full token values, add .env and fb_tokens_output.json to git ignores, and rotate any token that was printed, logged, or committed.

Risk: The token helper points users to a hard-coded Facebook app ID.

Mitigation: Replace the hard-coded app ID with the user's own configured FB_APP_ID before running token exchange or Page publishing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yunneetoichoi/skills/qwe)
- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python scripts and environment-variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Facebook app credentials, a Facebook Page ID, and a Page access token configured through environment variables.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
