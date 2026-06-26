## Description: <br>
Generate, update, and query Queenshow editor-next product detail pages through the Queenshow OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiongwang11](https://clawhub.ai/user/xiongwang11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ecommerce operators use this skill to generate, update, and inspect Queenshow product detail pages from product media, copy, SKU information, and style requirements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product media and detail-page content are sent to Queenshow during normal use. <br>
Mitigation: Use the skill only for content approved for Queenshow processing and review selected media before upload. <br>
Risk: API keys may be exposed if supplied directly on command lines or shared logs. <br>
Mitigation: Prefer environment variables, stdin, or a secret file; use a least-privilege key and rotate it if exposure is suspected. <br>
Risk: Production content generation may consume wallet balance or fail before completion. <br>
Mitigation: Check usage and quota before batch runs, poll task status, and verify the final document before relying on generated pages. <br>


## Reference(s): <br>
- [Queenshow Detail Page OpenAPI](artifact/references/openapi.md) <br>
- [Queenshow Detail Page Generator on ClawHub](https://clawhub.ai/xiongwang11/queenshow-detail-page) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, and API workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Queenshow API calls and JSON responses through the bundled client.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
