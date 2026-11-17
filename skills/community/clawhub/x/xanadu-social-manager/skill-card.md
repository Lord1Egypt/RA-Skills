## Description:

Use this skill when the user wants to manage social media scheduling, analytics, cross-posting, or AI-assisted content creation across Instagram, TikTok, Twitter/X, LinkedIn, or Facebook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saintlittlefish](https://clawhub.ai/user/saintlittlefish)

### License/Terms of Use:


## Use Case:

External users and social media operators use this skill to plan posts, adapt content across platforms, generate approved replies, and summarize social media analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a hardcoded SkillPay API key in billing configuration.

Mitigation: Remove the bundled key, rotate it before release, and require deployers to provide their own billing credentials through configuration or environment variables.

Risk: The billing module can submit charge requests for skill usage.

Mitigation: Require explicit user or deployer consent before enabling billing and before any charge is made.

Risk: Scheduled post content is stored locally in queue.json.

Mitigation: Document local storage behavior and apply appropriate access controls, retention limits, or encryption for sensitive social content.

## Reference(s):

- [Platform Specifications](references/platform-specs.md)
- [Caption Templates](assets/templates/captions.md)
- [SkillPay](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce social copy, scheduling recommendations, analytics summaries, platform-specific formatting, and configuration guidance.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter is 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
