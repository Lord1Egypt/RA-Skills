## Description:

Generates AI images from text prompts with YouMind's multi-model API and saves generated images to a YouMind board.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dophinl](https://clawhub.ai/user/dophinl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate images from natural-language prompts through the YouMind CLI. The skill returns generated image URLs in chat and stores the images on the user's YouMind board.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install a persistent global YouMind npm CLI.

Mitigation: Install and review a pinned CLI version yourself before enabling the skill.

Risk: Image prompts and generated images are sent to and saved by YouMind.

Mitigation: Avoid sensitive prompts and confirm YouMind storage, retention, and deletion behavior before use.

Risk: Image generation uses polling and background task behavior that can continue after the first response.

Mitigation: Keep the documented polling timeout and review returned image URLs before sharing or reusing outputs.

Risk: The skill includes vendor promotional and upgrade messaging.

Mitigation: Review user-facing messages for policy fit before deploying the skill in managed environments.

## Reference(s):

- [Setup](references/setup.md)
- [Error Handling](references/error-handling.md)
- [Long-Running Tasks](references/long-running-tasks.md)
- [YouMind CLI package](https://www.npmjs.com/package/@youmind-ai/cli)
- [YouMind API keys](https://youmind.com/settings/api-keys?utm_source=youmind-image-generator)
- [YouMind issue tracker](https://github.com/YouMindInc/youmind/issues)
- [ClawHub skill page](https://clawhub.ai/dophinl/skills/youmind-image-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown chat responses with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns generated image URLs; may include setup, timeout, error, paywall, and follow-up guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
