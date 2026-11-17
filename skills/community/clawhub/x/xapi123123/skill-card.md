## Description:

Use xapi CLI to access real-time external data including Twitter/X profiles, tweets, timelines, crypto token prices and metadata, web search, news, and AI text processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glacier-luo](https://clawhub.ai/user/glacier-luo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover xapi actions, inspect their schemas, and run CLI calls for external data, search, crypto, social, and text-processing services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run an unpinned remote npm CLI through npx.

Mitigation: Use a pinned and reviewed xapi-to package version before deployment.

Risk: The skill can send selected prompts, queries, and API inputs to xapi and connected third-party services.

Mitigation: Review requested calls before use and avoid sending sensitive or confidential content unless approved.

Risk: OAuth binding, posting, payment, top-up, and persistent API-key behavior can have account or financial impact.

Mitigation: Run OAuth, posting, and payment-related commands only after explicit user intent, and protect stored API keys and top-up URLs.

## Reference(s):

- [xAPI homepage](https://xapi.to)
- [ClawHub skill page](https://clawhub.ai/glacier-luo/skills/xapi123123)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with bash command examples; xapi CLI responses are JSON by default.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx and an XAPI_API_KEY; some actions may require OAuth binding or account balance.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
