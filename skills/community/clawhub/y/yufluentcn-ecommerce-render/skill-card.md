## Description:

Renders cross-border ecommerce templates such as size charts, specification cards, feature grids, comparison tables, and promotional banners through Yufluent server-side Pillow rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and developers use this skill to turn structured product data into PNG product information graphics for marketplace listings and promotional banners.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product/template data, local file contents supplied as render data, API credentials, and rendering data can be sent to configurable network endpoints.

Mitigation: Use only trusted Yufluent endpoints, keep TOKENAPI_BASE_URL unset unless the destination is fully trusted, avoid non-local plaintext HTTP, and submit only intended non-sensitive JSON data.

Risk: Rendered ecommerce graphics can contain incorrect or misleading product claims if the supplied product facts are inaccurate.

Mitigation: Review the structured render data and final output against product facts before publication.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/metahuan/skills/yufluentcn-ecommerce-render)
- [Yufluent homepage](https://claw.changzhiai.com)
- [Yufluent OpenClaw integration](https://claw.changzhiai.com/app/openclaw)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown or JSON responses from CLI/API execution, typically describing server-rendered PNG output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENAPI_KEY; render inputs are submitted to the configured Yufluent endpoint.]

## Skill Version(s):

1.1.2 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
