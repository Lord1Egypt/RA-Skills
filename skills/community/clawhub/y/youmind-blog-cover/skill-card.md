## Description:

Generates 16:9 blog cover and article header images from a title, topic, or URL using the YouMind CLI and image generation service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dophinl](https://clawhub.ai/user/dophinl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create text-friendly 16:9 cover images for blog posts, article headers, thumbnails, or featured images from a title, topic, or URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad local command authority for YouMind CLI usage and package installation.

Mitigation: Review or narrow allowed commands before use and approve local shell execution only when the requested action is expected.

Risk: The workflow uses a mutable global installation of the YouMind CLI.

Mitigation: Prefer an audited or pinned CLI installation where possible before running the skill in managed environments.

Risk: The skill depends on a YouMind API key, remote service access, and remote board storage.

Mitigation: Set API keys outside chat, avoid passing secrets in command-line arguments, and review content sensitivity before sending titles, URLs, or topics to the service.

Risk: The user experience can include branded YouMind links, upsell messages, and plan-limit handling.

Mitigation: Disclose the third-party service workflow to users and review promotional or upgrade messaging for the deployment context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dophinl/skills/youmind-blog-cover)
- [YouMind CLI](https://www.npmjs.com/package/@youmind-ai/cli)
- [YouMind Skills Gallery](https://youmind.com/skills?utm_source=youmind-blog-cover)
- [Setup](references/setup.md)
- [Error Handling](references/error-handling.md)
- [Long-Running Tasks](references/long-running-tasks.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with shell commands, status updates, generated image URLs, and YouMind board links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require polling for long-running image generation and stores generated images on a YouMind board.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
