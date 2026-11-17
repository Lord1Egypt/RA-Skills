## Description:

Standardizes building local AI social-media automation tools from requirements through Windows EXE delivery, with selector mapping templates for Xiaohongshu, Douyin, and Kuaishou.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cruciata](https://clawhub.ai/user/cruciata)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to create local Playwright and Ollama social-media auto-reply tools with platform-specific selector maps, dry-run validation, and Windows packaging steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated automation can post replies from logged-in social-media accounts.

Mitigation: Keep dry-run as the default, review generated replies, and require explicit confirmation before enabling real sends.

Risk: Generated code may preserve browser profiles or expose tokens and secrets if committed or packaged without review.

Mitigation: Inspect generated code and packaged artifacts for saved profiles, tokens, and secrets before committing, pushing, or distributing them.

Risk: Platform rules may restrict or prohibit automated replies.

Mitigation: Verify the target platform's rules before enabling automation for real accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cruciata/skills/social-auto-tool-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a dry-run-first workflow, platform selector mapping, validation gates, and Windows EXE packaging guidance.]

## Skill Version(s):

1.1.0 (source: evidence release and artifact/skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
