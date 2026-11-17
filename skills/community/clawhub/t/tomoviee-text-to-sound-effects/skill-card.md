## Description:

Generate sound effects from text prompts using the Tomoviee Text-to-Sound-Effect API through the Wondershare OpenAPI gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create Tomoviee text-to-sound-effect tasks, poll asynchronous task results, and retrieve generated audio URLs for sound effects or ambience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authentication helper can expose a reusable Tomoviee API token and secret through command output or shell history.

Mitigation: Avoid the quick-start token helper for sensitive credentials; keep secrets out of command-line arguments and logs, and prefer a secrets manager or environment-backed workflow.

Risk: The skill requires runtime access to Tomoviee/Wondershare API credentials and sends requests to an external API gateway.

Mitigation: Use only approved credentials and prompts, confirm the configured endpoint before use, and limit credential scope where possible.

Risk: Installing unpinned dependencies can introduce supply-chain or compatibility risk in production environments.

Mitigation: Install dependencies in an isolated environment and pin reviewed versions before production use.

## Reference(s):

- [Tomoviee Text-to-Sound-Effect API Reference](artifact/references/audio_apis.md)
- [Text-to-Sound-Effect Prompt Guide](artifact/references/prompt_guide.md)
- [Tomoviee Developer Portal](https://www.tomoviee.ai/developers.html)
- [Tomoviee API Documentation](https://www.tomoviee.ai/doc/)
- [ClawHub Skill Page](https://clawhub.ai/wondershare-boop/skills/tomoviee-text-to-sound-effects)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, API calls]

**Output Format:** [Markdown guidance with Python and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task IDs and, after polling, generated audio result URLs when valid Tomoviee/Wondershare API credentials are supplied.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
