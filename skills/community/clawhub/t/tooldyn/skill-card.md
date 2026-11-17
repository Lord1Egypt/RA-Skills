## Description:

Intent-based tool selection that recommends relevant OpenClaw tools for the latest user message and returns a short usage hint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peter7397](https://clawhub.ai/user/peter7397)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent operators use this skill to choose a smaller set of relevant tools for a user turn, especially in Feishu and Ollama-style setups where exposing all tools can increase context size and tool-loop risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can recommend powerful shell or write-style tools too broadly, and its output could be mistaken for authorization to expose or execute those tools.

Mitigation: Use an independent allowlist and require explicit user intent before shell, file write, or Feishu mutation tools are exposed or called.

## Reference(s):

- [Dynamic Tool on ClawHub](https://clawhub.ai/peter7397/skills/tooldyn)
- [Publisher profile](https://clawhub.ai/user/peter7397)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [JSON-like tool response with recommended tool names, a hint, and a short message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are keyword-based and capped at eight tools.]

## Skill Version(s):

1.0.0 (source: release evidence, manifest.json, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
