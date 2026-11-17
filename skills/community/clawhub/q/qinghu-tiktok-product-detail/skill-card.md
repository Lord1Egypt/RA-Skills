## Description:

按商品 ID 批量查询 TikTok Shop 商品详情，每次最多查询 10 个商品。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

TikTok Shop sellers and analysts use this skill to retrieve product details by ID, compare reported product metrics, and share concise results after approving any paid queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions can install and run external Node/qhkit tooling, including an unpinned latest version.

Mitigation: Review the installation first, prefer a pinned qhkit version, and avoid persistent PATH or profile changes unless intended.

Risk: The query requires a Qinghu API token and may incur Qinghu credit charges.

Mitigation: Handle the token securely, check current pricing, and obtain user approval before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-tiktok-product-detail)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Concise answers with product details and optional tabular export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid lookups require prior user approval; results may include per-call credit usage.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
