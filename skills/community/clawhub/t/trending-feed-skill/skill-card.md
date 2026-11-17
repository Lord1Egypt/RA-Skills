## Description:

GitHub订阅 helps agents retrieve GitHub Trending repository lists and prepare repository summaries, with optional language filtering for developer workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to request GitHub Trending repositories, optionally filter by language, and format the results for agent-driven updates or workflow notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the skill suspicious because its requested tools and described capabilities are broader than a simple GitHub Trending feed requires.

Mitigation: Review the skill before installing and grant it access only in a low-sensitivity workspace unless the publisher narrows the activation text and documents the commands, files, tokens, and caches it uses.

Risk: The artifact describes private-repository and Git-operation capabilities that are not supported by the server evidence for this release.

Mitigation: Treat the skill as a public Trending helper unless separate reviewed evidence confirms broader repository access behavior.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/trending-feed-skill)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository names, descriptions, languages, star counts, and URLs when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
