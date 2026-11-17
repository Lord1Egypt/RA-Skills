## Description:

Find and evaluate free/public APIs for projects, demos, agents, prototypes, data enrichment, examples, integrations, or research before writing integration code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[builtbyecho](https://clawhub.ai/user/builtbyecho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to shortlist public API candidates by category, authentication, HTTPS, CORS, and practical fit. It supports project prototyping, demos, integrations, data enrichment, examples, and research before integration work begins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The npm command installs and runs mutable package code at execution time.

Mitigation: Use the bundled local fallback or a pinned, reviewed npm version, and run it without unnecessary credentials in the environment.

Risk: The optional Vaultline workflow can store API research with a third-party service.

Mitigation: Use Vaultline only after explicit approval to store the research content, and avoid exposing sensitive notes or credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/builtbyecho/skills/public-api-finder)
- [Project homepage](https://github.com/BuiltByEcho/public-api-finder)
- [public-api-lists API data](https://public-api-lists.github.io/public-api-lists/api/all.json)
- [BuiltByEcho production x402 endpoint](https://x402.bankr.bot/0x2a16625fad3b0d840ac02c7c59edea3781e340ae/public-api-finder)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown API recommendations with optional JSON CLI output and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations include API name, URL, fit, auth requirement, HTTPS/CORS notes, caveats to verify, example requests after checking docs, and OpenAPI URL when available.]

## Skill Version(s):

0.5.11 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
