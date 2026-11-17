## Description:

Chat with AI companions on Velora for platform testing, companion interaction, and companion image generation through Playwright browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darkatek7](https://clawhub.ai/user/darkatek7)

### License/Terms of Use:

MIT-0

## Use Case:

External users, QA testers, and developers use this skill to automate Velora login, companion chat, image request, and basic platform verification workflows with their own account credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live Velora account credentials and examples pass passwords as command-line arguments.

Mitigation: Use a test account when possible and prefer environment variables or a secure prompt instead of passing passwords on the command line.

Risk: The browser automation can perform real login, messaging, and image request actions on a user account.

Mitigation: Review the script before installation and confirm each login, message, and image request before running it on a real account.

## Reference(s):

- [Velora Companions Reference](references/companions.md)
- [Velora Login](https://velora.cloudm8.net/login)
- [ClawHub Skill Page](https://clawhub.ai/darkatek7/skills/velora)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JavaScript and shell command examples, plus JSON-like script result objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Velora credentials, Node.js, Playwright, and Chromium; browser automation can perform live account actions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
