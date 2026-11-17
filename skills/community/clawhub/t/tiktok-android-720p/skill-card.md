## Description:

Automates TikTok search, commenting, likes, favorites, and publishing on 720x1280 Android devices through ADB, with optional AI-generated comments using Claude, GPT-4, or OpenRouter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[molin-g](https://clawhub.ai/user/molin-g)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to run ADB-driven TikTok search, engagement, AI comment generation, and publishing workflows on controlled 720p Android devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publish mode can delete videos from the connected Android device camera roll.

Mitigation: Review and remove or constrain publish-mode camera cleanup before use; avoid running publish mode on personal devices or accounts unless media is backed up.

Risk: Unsafe ADB shell input handling can execute unintended commands on a connected Android device.

Mitigation: Add strict validation or safe argument handling for device IDs, topics, descriptions, file paths, URLs, and other values passed into ADB shell commands.

Risk: Executable config files and plaintext environment files can expose AI provider API keys.

Mitigation: Use environment-managed secrets where possible, keep local config and .env files out of version control, and rotate keys if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/molin-g/skills/tiktok-android-720p)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ADB and Python commands, device setup steps, API key configuration guidance, and operational cautions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
