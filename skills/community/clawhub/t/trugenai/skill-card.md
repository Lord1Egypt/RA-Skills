## Description:

Build, configure, and deploy conversational video agents using the Trugen AI platform API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajayk47](https://clawhub.ai/user/ajayk47)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create, configure, embed, and operate Trugen conversational video agents, including knowledge bases, webhooks, LiveKit integration, tools, MCPs, multilingual settings, and custom LLM connections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if browser widget examples are copied with real credentials.

Mitigation: Keep Trugen management API keys server-side, use a server-side proxy for client embeds, and scope and rotate keys.

Risk: Recording and webhook callbacks can process sensitive conversation data.

Mitigation: Disable recording unless it is explicitly needed and consented to, and secure webhook handlers with HTTPS, authentication, signing checks, or IP restrictions.

Risk: Update and delete API examples can change or remove account resources.

Mitigation: Review IDs and payloads before execution, test changes outside production, and use least-privilege credentials where available.

## Reference(s):

- [Trugen AI documentation](https://docs.trugen.ai/docs/overview)
- [Trugen API reference](https://docs.trugen.ai/api-reference/overview)
- [Trugen developer portal](https://app.trugen.ai)
- [Agents API Reference](references/agents.md)
- [Embedding & Integration Reference](references/embedding.md)
- [Knowledge Base API Reference](references/knowledge-base.md)
- [Persona Templates API Reference](references/templates.md)
- [Tools & MCPs API Reference](references/tools-and-mcps.md)
- [Webhooks & Callbacks Reference](references/webhooks.md)
- [Providers, Avatars & Multilingual Reference](references/providers-avatars-languages.md)
- [Prompting Strategies & Use Cases](references/prompting-and-use-cases.md)
- [Deepgram STT models](https://developers.deepgram.com/docs/models-languages-overview#nova-3)
- [ElevenLabs TTS languages](https://elevenlabs.io/docs/overview/capabilities/text-to-speech#supported-languages)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with API examples and inline JSON, bash, HTML, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Trugen endpoint examples, embed snippets, webhook handlers, and configuration recommendations.]

## Skill Version(s):

1.0.1 (source: frontmatter, release evidence, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
