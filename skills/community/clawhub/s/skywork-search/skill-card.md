## Description:

Skywork Search helps an agent search the web for current information through the Skywork Search API and return sourced snippets for research, fact lookup, recent events, and document preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gxcun17](https://clawhub.ai/user/gxcun17)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users can use this skill when an agent needs up-to-date web research, recent facts, statistics, news, or source material before answering a user or drafting content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to the Skywork API and may include sensitive user or business context.

Mitigation: Use the skill only for queries appropriate to send to Skywork, and avoid submitting secrets, regulated data, or confidential material unless approved for that service.

Risk: The skill requires a Skywork API key, which could be exposed through shell history, logs, or configuration files if handled carelessly.

Mitigation: Prefer OpenClaw-managed API-key configuration, avoid printing or sharing the key, and restrict access to any file that stores it.

Risk: Search results depend on Skywork API availability, result quality, and a 30-second per-query timeout.

Mitigation: Check returned source URLs and snippets before relying on facts, and retry or use alternate research paths when the API fails or results are incomplete.

## Reference(s):

- [Skywork Search on ClawHub](https://clawhub.ai/gxcun17/skills/skywork-search)
- [Skywork API Key Setup Guide](references/apikey-fetch.md)
- [Skywork](https://skywork.ai)
- [Skywork API Key Settings](https://skywork.ai/?openApiKeySetting=1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and text files containing query results, source URLs, and snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts one to three search queries per invocation; each query has a 30-second timeout and depends on Skywork API availability.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
