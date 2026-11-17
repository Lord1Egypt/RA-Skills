## Description:

Provides six-stage Shopify store operations guidance for sourcing, supplier evaluation, listings, store decoration, social content, and monitoring reviews through the Yufluent cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and their agents use this skill to collect store context and request Markdown operating plans for Shopify product selection, supplier checks, listing optimization, store presentation, social planning, and performance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send TOKENAPI_KEY and store or business context to a configurable Yufluent endpoint.

Mitigation: Use only a trusted HTTPS Yufluent endpoint or a loopback development proxy, keep TOKENAPI_KEY private, and avoid sending customer or payment data in prompts.

Risk: Local import paths can load sibling _shared code when the installation directory is writable by untrusted users.

Mitigation: Install the skill in a trusted directory and restrict write access to sibling shared-code paths.

Risk: Operational plans and marketing copy can be inaccurate or unsuitable for a target market.

Mitigation: Review generated plans before execution and verify claims, suppliers, listings, promotions, and compliance obligations manually.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluentcn-shopify-operator)
- [Yufluent console](https://claw.changzhiai.com)
- [OpenClaw setup](https://claw.changzhiai.com/app/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text returned from the Yufluent skill run, with optional CLI metadata on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENAPI_KEY and may use TOKENAPI_BASE_URL to select the Yufluent endpoint.]

## Skill Version(s):

1.1.2 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
