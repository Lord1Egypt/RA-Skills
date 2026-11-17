## Description:

Runs a local bridge that connects OpenAI-compatible clients to api.a7w.cn for chat, speech, image generation, subtitles, and other application tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Developers connect OpenAI-compatible AI clients and workflows to api.a7w.cn through a local bridge for chat, speech, transcription and subtitles, image generation, and other application tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unauthenticated bridge exposed beyond the local machine could allow others to use paid API access.

Mitigation: Keep the bridge bound to localhost and stop it when unused; add authentication and access controls before any wider exposure.

Risk: API credentials may be misused or incur unexpected charges if shared.

Mitigation: Use your own key, never accept shared keys, keep credentials private, and set spending quotas.

Risk: Requests and data are sent to api.a7w.cn and any configured embedding provider.

Mitigation: Use the bridge only when you intend to route that traffic through those services.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/2253128/skills/sanjianke-a7w-bridge)
- [a7w API documentation](https://api.a7w.cn/docs.html)
- [Integration recipes](references/integrate.md)
- [Launcher instructions](references/launcher.md)

## Skill Output:

**Output Type(s):** [Configuration instructions, Shell commands, Code, Guidance]

**Output Format:** [Markdown with configuration and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local bridge can return JSON, audio, image URLs, and SRT/VTT subtitles.]

## Skill Version(s):

1.1.1 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
