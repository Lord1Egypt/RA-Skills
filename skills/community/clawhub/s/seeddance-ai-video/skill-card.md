## Description:

Integrates the ByteDance SeedDance AI video generation API for text-to-video, image-to-video, style transfer, batch generation, webhook, and error-handling guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashwinramachandran2002](https://clawhub.ai/user/ashwinramachandran2002)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure SeedDance API access and adapt example code for generating, transforming, batching, and receiving callbacks for AI video tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing an unverified or floating seeddance-sdk package version can introduce supply-chain risk.

Mitigation: Verify that seeddance-sdk is the official SDK before use and pin a reviewed package version.

Risk: SEEDDANCE_API_KEY can grant access to the external video generation service if exposed.

Mitigation: Keep the API key scoped to the intended use case and out of source control.

Risk: Prompts, uploaded media, generated outputs, and webhook metadata may be sent to external services.

Mitigation: Avoid submitting sensitive or regulated content unless external processing is approved for the use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ashwinramachandran2002/skills/seeddance-ai-video)
- [SeedDance console](https://console.seeddance.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON, bash, environment variable, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SDK installation commands, configuration snippets, API usage examples, webhook patterns, and error-handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
