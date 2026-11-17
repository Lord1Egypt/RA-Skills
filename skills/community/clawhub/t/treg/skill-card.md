## Description:

treg helps agents discover and call external data APIs, connected account tools, and team-registered credentials for SEO, SERP, backlinks, social trends, enrichment, ads, scraping, and related live-data workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superdesigndev](https://clawhub.ai/user/superdesigndev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use treg to find live external data or connected account capabilities, inspect parameters and pricing, and execute calls through catalog endpoints or team-registered tools. It is most relevant when the agent needs API-backed market, search, social, enrichment, ads, scraping, or account-management actions without directly handling provider keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to install and authenticate a CLI that can broker long-lived access to external accounts and team tools.

Mitigation: Install only if the publisher is trusted, inspect the installer before running it, and prefer scoped agent tokens for agent or CI use.

Risk: Catalog calls can spend prepaid balance, and connected tools may take account actions such as publishing, ad management, secret uploads, CLI execution, or organization changes.

Mitigation: Confirm prices before paid calls and require separate human confirmation before paid calls, secret uploads, CLI execution, social or ads actions, and organization changes.

Risk: Broad approval for all treg commands can allow more authority than intended for a specific task.

Mitigation: Avoid blanket approval; restrict credential imports to explicit files or directories and review the requested command scope before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superdesigndev/skills/treg)
- [treg agent onboarding](https://treg.to/llms.txt)
- [treg interactive tutorial](https://treg.to/tutorial)
- [treg service endpoint](https://treg.to)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prices, endpoint parameters, command sequences, API request examples, and account-action guidance.]

## Skill Version(s):

0.11.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
