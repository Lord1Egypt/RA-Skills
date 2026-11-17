## Description:

Full SEO content automation via MCP. Audit websites, check Google rankings, discover site structure, auto-select keywords matched to your DR, research and swap keywords, generate full articles with images and JSON-LD, publish to WordPress or webhook, track keyword rankings and competitors - all from your terminal or IDE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kwesi-dev](https://clawhub.ai/user/kwesi-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an MCP-compatible agent to SEO Ladders for technical SEO audits, ranking checks, site discovery, keyword research, content planning, article generation, publishing, and refresh monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content or invoke CMS webhooks through remote SEO automation tools.

Mitigation: Require human approval before publishing, invoking webhooks, or making CMS changes, and use least-privileged CMS or webhook credentials.

Risk: The skill can modify content calendar entries and perform update or delete actions.

Mitigation: Configure the MCP client or agent to ask for confirmation before changing calendar entries or deleting/updating content.

Risk: The skill can save generated content locally, which may place files in sensitive or synced repositories.

Mitigation: Save generated files only to intended directories and avoid sensitive or synced repositories unless that storage is deliberate.

Risk: Using the skill gives SEO Ladders API-key access to the MCP client and remote service.

Mitigation: Install only when the remote service is trusted for the intended SEO workflow and protect the SEO_LADDERS_API_KEY as a secret.

## Reference(s):

- [Seo Ladders ClawHub Skill](https://clawhub.ai/kwesi-dev/skills/seo-ladders)
- [SEO Ladders](https://seoladders.com)
- [SEO Ladders MCP Features](https://seoladders.com/features/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, JSON-like structured results, configuration snippets, and status text returned through MCP tools.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some workflows are asynchronous and require polling job status before final results are available.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
