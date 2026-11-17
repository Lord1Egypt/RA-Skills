## Description:

An MCP-compatible remote random-value generation service for AI applications, LLMs, and systems that need high-quality random values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to request integers, floats, bytes, UUIDs, strings, choices, and booleans from a remote random-generation API after configuring an XBY API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XBY API key in a local plaintext .env file.

Mitigation: Use only trusted local workspaces, restrict file access, avoid committing .env files, and rotate the key if it may have been exposed.

Risk: The remote random-number service can receive generated values that users may treat as secrets.

Mitigation: Do not use this skill to create passwords, API tokens, encryption keys, recovery codes, nonces, or other confidential security material unless the provider trust and retention model is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/random-generator)
- [Publisher profile](https://clawhub.ai/user/alinklab)
- [XiaoBenYang service](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON, API calls, configuration]

**Output Format:** [Text summary of remote API JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY API key configured in the environment or a local .env file before use.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
