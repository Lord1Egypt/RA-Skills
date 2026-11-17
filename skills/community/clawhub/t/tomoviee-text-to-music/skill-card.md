## Description:

Generate background music from text prompts using the Tomoviee Text-to-Music API through the Wondershare OpenAPI gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to generate background music from text prompts with duration and quantity controls, then retrieve asynchronous Tomoviee task results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tomoviee API prompts and credentials are sent to Wondershare/Tomoviee services.

Mitigation: Use the skill only for text-to-music requests and avoid sending sensitive prompts or secrets unless the service terms and data handling are acceptable.

Risk: Credentials can be exposed when passed to the documented auth-token helper on the command line.

Mitigation: Use a secret manager, protected environment variables, or an interactive secret prompt, and rotate credentials that may already have been exposed in terminals, logs, CI, or agent traces.

Risk: The package includes guidance for unrelated media APIs.

Mitigation: Treat text-to-music behavior as the supported scope and review unrelated API guidance before using it.

## Reference(s):

- [Tomoviee Text-to-Music API Reference](references/audio_apis.md)
- [Tomoviee Prompt Engineering Guide](references/prompt_guide.md)
- [Tomoviee Developer Portal (Global)](https://www.tomoviee.ai/developers.html)
- [Tomoviee API Docs (Global)](https://www.tomoviee.ai/doc/)
- [Tomoviee Developer Portal (Mainland)](https://www.tomoviee.cn/developers.html)
- [Tomoviee API Docs (Mainland)](https://www.tomoviee.cn/doc/)
- [Wondershare OpenAPI Gateway](https://openapi.wondershare.cc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Tomoviee task identifiers, task status data, and generated audio URLs through API responses.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
