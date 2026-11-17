## Description:

Helps an agent query Wisgate model pricing, capabilities, and API compatibility, then prepare OpenClaw model configuration updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flofrie](https://clawhub.ai/user/flofrie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to look up Wisgate-hosted model metadata and prepare model entries for OpenClaw configuration. It is intended for adding models, comparing pricing, and checking Anthropic, OpenAI, or Google API compatibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents to update OpenClaw model configuration.

Mitigation: Require review before configuration edits and verify model IDs, API type, context window, token limits, and pricing against MODELS.json or Wisgate.

Risk: The skill can lead agents to use a stored Firecrawl API key through an external script for Wisgate lookups.

Mitigation: Require explicit approval before network calls, avoid exposing TOOLS.md, and verify the referenced firecrawl-search script before giving it an API key.

## Reference(s):

- [Wisgate model detail pages](https://wisgate.ai/models/MODEL_ID)
- [Wisgate Anthropic-compatible API base](https://api.wisgate.ai/)
- [Wisgate OpenAI-compatible API base](https://api.wisgate.ai/v1)
- [Wisgate Google-compatible API base](https://api.wisgate.ai/v1beta)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to MODELS.json and openclaw.json; network lookup guidance can involve Firecrawl.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
