## Description:

Generate and remix images with Flux through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to create or remix Flux images through RunAPI. It guides agents to use the RunAPI CLI for one-off image generation and RunAPI SDK references for app or backend integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the RunAPI Homebrew tap and CLI, which will handle RunAPI authentication and submitted media.

Mitigation: Confirm the RunAPI tap and CLI are trusted before installation, protect API keys or CLI config, and review paid task submissions before authorizing them.

Risk: RunAPI task submission can consume paid service capacity or send user media to an external service.

Mitigation: Submit each task only after validating the discovered contract and request JSON, and do not retry or resubmit paid work unless the evidence shows it is safe or the user authorizes it.

## Reference(s):

- [RunAPI Flux homepage](https://runapi.ai/models/flux)
- [Model overview, pricing, and rate limits](https://runapi.ai/models/flux.md)
- [Provider overview](https://runapi.ai/providers/black-forest-labs.md)
- [Full model catalog](https://runapi.ai/models.md)
- [SDK integration](https://github.com/runapi-ai/flux-sdk)
- [Flux 2 Klein variant](https://runapi.ai/models/flux/2-klein.md)
- [Flux Dev variant](https://runapi.ai/models/flux/dev.md)
- [Flux Pro variant](https://runapi.ai/models/flux/pro.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON request files, and SDK integration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce or verify image media deliverables through RunAPI task responses.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
