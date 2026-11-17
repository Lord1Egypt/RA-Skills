## Description:

Searches and retrieves Spanish Wikitolica encyclopedia articles about Catholic doctrine, saints, popes, theology, church history, liturgy, sacraments, and biblical studies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cursocatolico](https://clawhub.ai/user/cursocatolico)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find Spanish Catholic encyclopedia entries and retrieve sourced article text with attribution. It is intended for questions about Catholic doctrine, history, saints, popes, theology, liturgy, sacraments, and biblical studies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests unrestricted Bash access even though its lookup workflow only needs scoped Wikitolica retrieval.

Mitigation: Review before installation and prefer scoped Fetch or MCP access for Wikitolica pages instead of unrestricted shell execution.

Risk: Direct HTTP lookup can produce incorrect article URLs if slugs are guessed.

Mitigation: Use MCP search results or the sitemap to confirm slugs before citing article URLs.

Risk: Wikitolica article content has attribution and CC BY-SA 4.0 expectations in the artifact workflow.

Mitigation: Preserve the Wikitolica attribution line and source URL when returning article content.

## Reference(s):

- [Wikitolica](https://www.wikitolica.com)
- [ClawHub skill page](https://clawhub.ai/cursocatolico/skills/wikitolica)
- [Publisher profile](https://clawhub.ai/user/cursocatolico)
- [Zenodo DOI](https://doi.org/10.5281/zenodo.19387074)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Spanish Markdown or text with Wikitolica attribution and source URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses real Wikitolica slugs from MCP results or the sitemap; responses should stay in Spanish.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
