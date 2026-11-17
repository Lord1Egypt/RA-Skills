## Description:

Fetches or reads user-provided URLs through a local 9Router backup web fetch service when the primary 9router-web-search skill fails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to fetch URL content through the local 9Router backup service when the primary web search skill is unavailable or explicitly bypassed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted URLs can trigger unintended access through the local fetch service.

Mitigation: Confirm unfamiliar URLs before fetching and restrict use to intended targets.

Risk: Bearer tokens can be exposed if pasted into prompts, commands, or logs.

Mitigation: Keep NINEROUTER_KEY in the environment and avoid hardcoding tokens in commands or output.

Risk: The skill depends on the local 9Router backup service being available on localhost:20128.

Mitigation: Check service availability before use and report fallback options when the endpoint is down.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmuhammadagus-byte/skills/web-search-9routers-backup)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include URL fetch parameters, local service checks, token handling guidance, and error-handling advice.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
