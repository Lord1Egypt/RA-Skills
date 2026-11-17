## Description:

Use the we-promise/sure REST API with X-Api-Key auth. Covers accounts, transactions, categories, tags, merchants, imports, holdings, trades, valuations, chats, official docs URLs, self-update workflow from upstream OpenAPI, and ClawHub publish readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashanzzz](https://clawhub.ai/user/ashanzzz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and operate Sure financial-account resources through authenticated REST API calls, including accounts, transactions, categories, tags, merchants, imports, holdings, trades, valuations, and chats. It supports common CLI wrappers plus raw official endpoint access for less-common Sure API operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose broad financial-account actions through the Sure API.

Mitigation: Install only with a restricted Sure API key and review write requests before execution.

Risk: Credential-forwarding paths can expose Sure API access if secrets are placed in prompts, command-line arguments, or non-secure files.

Mitigation: Keep SURE_API_KEY in secure environment storage and do not pass it as a command-line argument or paste it into chat.

Risk: The raw request wrapper can reach destructive endpoints such as account deletion, reset, auth, or other sensitive API paths.

Mitigation: Avoid raw wrapper calls for destructive or auth endpoints unless the exact method, path, and body have been explicitly reviewed and approved.

Risk: Untrusted prompts could redirect requests through a malicious base URL or arbitrary curl options.

Mitigation: Use a trusted SURE_BASE_URL and do not allow untrusted content to choose base URLs or extra curl arguments.

## Reference(s):

- [Sure OpenAPI specification](references/openapi.yaml)
- [Sure API endpoint summary](references/api_endpoints_summary.md)
- [Official Sure API docs directory](https://github.com/we-promise/sure/tree/main/docs/api)
- [Official Sure OpenAPI page](https://github.com/we-promise/sure/blob/main/docs/api/openapi.yaml)
- [ClawHub skill page](https://clawhub.ai/ashanzzz/skills/sure-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON request bodies, and API response summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce live Sure API calls when the agent executes bundled scripts; secrets are expected from secure environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
