## Description:

Generate and remix images with Flux 2 through RunAPI for one-off CLI workflows or SDK-based application integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through Flux 2 image generation and image remixing on RunAPI, including contract discovery, request construction, task execution, and deliverable verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may submit paid image-generation requests through a user's RunAPI account or API key.

Mitigation: Authenticate intentionally, inspect the generated request, and submit only when the user has approved the RunAPI action.

Risk: Prompts or local media included in a request may be uploaded to RunAPI.

Mitigation: Use only media intended for RunAPI processing and review request.json before submission when inputs are sensitive.

Risk: A stale CLI catalog or mismatched API contract can produce invalid requests or unverifiable outputs.

Mitigation: Use the installed CLI help and current API reference as the contract sources, then stop and report mismatches instead of guessing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/runapi-ai/skills/runapi-flux-2)
- [RunAPI Flux 2 Homepage](https://runapi.ai/models/flux-2)
- [Flux 2 Model Overview, Pricing, and Rate Limits](https://runapi.ai/models/flux-2.md)
- [Black Forest Labs Provider Overview](https://runapi.ai/providers/black-forest-labs.md)
- [RunAPI Model Catalog](https://runapi.ai/models.md)
- [Flux 2 SDK Integration](https://github.com/runapi-ai/flux-2-sdk)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, JSON, files]

**Output Format:** [Markdown guidance with shell commands, JSON request and response files, SDK code guidance, and downloaded image deliverables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the RunAPI CLI for one-off generation and may use RUNAPI_API_KEY or saved RunAPI CLI authentication.]

## Skill Version(s):

0.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
