## Description:

Shopify full-store operations coach that guides sourcing, supplier evaluation, listing optimization, store decoration, social planning, and monitoring through the Yufluent cloud harness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External Shopify operators and ecommerce developers use this skill to obtain guided operating plans for new-store launch and existing-store optimization across sourcing, suppliers, listings, decoration, social content, and monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token and Shopify business context are sent to the configured Yufluent cloud endpoint.

Mitigation: Set TOKENAPI_BASE_URL only to a trusted endpoint, prefer HTTPS, and limit submitted store data to what the workflow needs.

Risk: The local wrapper depends on helper modules resolved from the skill directory layout, which can be unsafe in shared or writable installations.

Mitigation: Install and run the skill only from a trusted local skill directory and avoid shared or writable parent directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluent-clawhub-publish-yufluentcn-shopify-operator)
- [Yufluent console](https://claw.changzhiai.com)
- [OpenClaw integration](https://claw.changzhiai.com/app/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown operating plans, structured checklists, templates, and CLI/API invocation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENAPI_KEY; sends store URL, niche, message, language, and business context to the configured Yufluent cloud endpoint.]

## Skill Version(s):

1.1.2 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
