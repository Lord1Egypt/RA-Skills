## Description:

Routes natural-language requests into SQL, SPARQL, SPASQL, SPARQL-FED, and GraphQL queries against OpenLink data spaces and knowledge graphs, returning tabulated results with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kidehen](https://clawhub.ai/user/kidehen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and knowledge-graph practitioners use this skill to turn natural-language requests into live SQL, SPARQL, SPASQL, SPARQL-FED, or GraphQL queries for OpenLink endpoints and related data spaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad network and query authority against live database and knowledge-graph services.

Mitigation: Use endpoint allowlists, read-only credentials, and explicit approval before non-default, authenticated, or externally supplied routes are used.

Risk: Prompts or generated queries may expose private prompts, internal endpoint URLs, proprietary graph names, or sensitive article titles to live services.

Mitigation: Avoid sensitive inputs unless privacy controls are in place, and require literal and IRI escaping before executing generated queries.

## Reference(s):

- [Protocol Routing Reference](artifact/references/protocol-routing.md)
- [Query Templates Reference](artifact/references/query-templates.md)
- [OpenLink AI Layer (OPAL)](https://opal.openlinksw.com)
- [OpenLink Virtuoso Platform](https://virtuoso.openlinksw.com)
- [Data Twingler GPT Store](https://chatgpt.com/g/g-z8YBujVdf-openlink-data-twingler)
- [OpenLink AI Agent Repository](https://github.com/OpenLinkSoftware)
- [ClawHub Skill Page](https://clawhub.ai/kidehen/skills/sql-sparql-graphql-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with query snippets, shell commands, tabulated results, and citation links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact live SQL, SPARQL, GraphQL, REST, MCP, or OPAL endpoints depending on route and configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
