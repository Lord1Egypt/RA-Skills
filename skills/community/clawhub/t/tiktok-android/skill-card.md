## Description:

Automates TikTok engagement on Android via ADB by searching topics, navigating videos, and posting static or AI-generated comments with a setup wizard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mladjan](https://clawhub.ai/user/mladjan)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to configure and run Android-based TikTok commenting sessions against search topics or the For You feed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control a logged-in TikTok account and post comments publicly.

Mitigation: Review the code and planned comments before execution, add explicit confirmation or dry-run controls before scheduled runs, and start with low-volume tests.

Risk: AI mode can send captured TikTok screenshots to external AI providers.

Mitigation: Use static-comment mode when screenshot sharing is not acceptable, or verify provider data handling before enabling AI-generated comments.

Risk: API keys may be stored locally in plaintext environment files.

Mitigation: Protect local .env files, keep them out of version control and shared archives, and prefer managed secret storage where available.

Risk: The security summary identifies unsafe input-handling flaws.

Mitigation: Avoid untrusted topic and comment inputs until the input handling is reviewed and patched.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mladjan/skills/tiktok-android)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide setup of local configuration, ADB device selection, static templates, and optional AI-provider credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
