## Description:

Resolves Telegram media placeholders into local files for agent vision or analysis by downloading the referenced Telegram media through the Bot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kurinzo](https://clawhub.ai/user/kurinzo)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to resolve Telegram media placeholders from chat context into local files that can be passed to image tools, analysis workflows, or shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target Telegram messages may be briefly forwarded while resolving media.

Mitigation: Use only trusted Telegram chats and bot credentials, and prefer a private forward-to chat when resolving media.

Risk: Downloaded files may be written outside the intended output folder if filenames are not safely constrained.

Mitigation: Run the skill with an isolated output directory and review publisher fixes for filename sanitization before routine use.

Risk: Bot tokens passed on the command line may be exposed through local process inspection or shell history.

Mitigation: Avoid routine use until token handling is changed to a safer secret source.

Risk: Forwarded-message deletion is best effort, so cleanup failures may leave copied chat content behind.

Mitigation: Use a private forward-to destination and confirm cleanup behavior before handling sensitive media.

## Reference(s):

- [Telegram Bot API](https://api.telegram.org)
- [ClawHub skill page](https://clawhub.ai/kurinzo/skills/tg-media-resolve)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown with inline bash commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads Telegram media to a local output directory and prints the resulting file path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
