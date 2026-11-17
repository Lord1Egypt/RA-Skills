## Description:

Calls seven Doubao models on vwu.ai through an OpenAI-compatible chat completions API using a user-provided vwu.ai API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3273283](https://clawhub.ai/user/a3273283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to list and call vwu.ai-hosted Doubao chat and generation models from shell-based workflows. It is intended for users who already have a vwu.ai API key and want OpenAI-compatible model calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and API keys may be sent to an unintended endpoint if VWU_BASE_URL is set to an untrusted host.

Mitigation: Keep VWU_BASE_URL unset unless the alternate HTTPS endpoint is intentionally trusted, and rotate the API key if the script may have run with an untrusted base URL.

Risk: Prompts containing secrets, quotes, or multiline content may be exposed or mishandled by the chat request script.

Mitigation: Avoid putting secrets in prompts and use quote-safe, single-line prompts until request payloads are serialized robustly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a3273283/skills/vwu-doubao)
- [vwu.ai platform](https://vwu.ai)
- [Supported model list](artifact/models.txt)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VWU_API_KEY and uses an optional VWU_BASE_URL environment variable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
