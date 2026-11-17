## Description:

Generates images and videos through Banana, Sora, and VEO model relay workflows for creative media production.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuhongfeii2](https://clawhub.ai/user/xuhongfeii2)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to submit Banana image, Sora video, and VEO video generation tasks through a platform relay. It helps create image, video, and short-form drama assets while returning task IDs, watcher status, and generated media results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads prompts and optional media to the easyclaw.bar relay.

Mitigation: Install and run it only when the user trusts that relay and is comfortable sending the requested prompts and media there.

Risk: The skill uses platform and OpenClaw credentials for submissions, watchers, and completion delivery.

Mitigation: Prefer environment-scoped credentials, avoid placing secrets in commands or URLs, and rotate credentials if watcher output or logs expose them.

Risk: The skill can create background cron watchers that poll for task completion.

Mitigation: Confirm watcher creation is expected, track returned job IDs, and remove watchers after terminal task states or failed notification setup.

Risk: Completion delivery can write messages back into sessions.

Mitigation: Scope notifications to an explicit current-session token and review session-writing behavior before deployment.

Risk: The documented default relay and token portal use HTTP URLs.

Mitigation: Prefer a version or deployment configuration that enforces HTTPS for token handling and media-generation requests.

## Reference(s):

- [Setup](references/setup.md)
- [Platform Relay API](references/platform-api.md)
- [Model Guide](references/model-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON task responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task IDs, watcher status, generated media URLs, and setup notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
