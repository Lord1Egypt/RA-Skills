## Description:

Sayba Skill Market MCP Server — Discover, invoke, publish, and rate AI Agent skills on Sayba's marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saybanet](https://clawhub.ai/user/saybanet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this MCP server to search the Sayba marketplace, inspect skill details, invoke available skills, publish skills, rate skills, and review account-specific marketplace activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles account credentials and authenticated marketplace actions, including publishing, rating, viewing owned skills, viewing call history, and invoking paid skills.

Mitigation: Use a scoped Sayba API key, avoid sharing production credentials with untrusted agents, and confirm before allowing paid invocations or public marketplace changes.

Risk: The configurable SAYBA_BASE_URL can send credentials and requests to a custom marketplace endpoint.

Mitigation: Use the default HTTPS Sayba host unless operating a reviewed custom instance, and do not reuse production API keys with custom hosts.

Risk: The security verdict is suspicious because endpoint and installation safeguards are weak, even though no specific risk findings were reported.

Mitigation: Install only from a trusted Sayba package version, pin the npm package where possible, and review the package before deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/saybanet/skills/sayba-skill-market)
- [Sayba platform](https://ai.sayba.com)
- [npm package](https://www.npmjs.com/package/sayba-skill-market)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [MCP tool responses as text or JSON, plus setup guidance with shell commands and client configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated operations require SAYBA_API_KEY; SAYBA_BASE_URL can point the server at a custom Sayba instance.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
