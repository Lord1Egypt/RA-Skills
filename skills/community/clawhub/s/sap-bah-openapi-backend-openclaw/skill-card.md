## Description: <br>
Reliable SAP Business Accelerator Hub API spec downloader for OpenClaw that uses SAP_HUB_USERNAME and SAP_HUB_PASSWORD to log in through Playwright Chromium, downloads OpenAPI JSON/YAML and OData EDMX to /usr/download, validates payload signatures, and supports importing specs into APIConnectionToSAP categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SHENRUIYANG](https://clawhub.ai/user/SHENRUIYANG) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to download SAP Business Accelerator Hub API specifications and prepare them for OpenClaw or APIConnectionToSAP workflows. It can also scaffold backend modules from downloaded OpenAPI specifications after manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SAP credentials are required for browser login automation. <br>
Mitigation: Keep SAP_HUB_USERNAME and SAP_HUB_PASSWORD only in a protected runtime environment and do not package real credentials with the skill. <br>
Risk: The default output location /usr/download can require elevated filesystem permissions or create shared-location exposure. <br>
Mitigation: Prefer a user-owned output directory when possible and review file permissions before running downloads. <br>
Risk: Generated backend code from OpenAPI input may be incomplete or unsafe for direct project inclusion. <br>
Mitigation: Inspect generated backend code before adding it to a project and avoid running the scaffolder on untrusted OpenAPI specs without manual review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SHENRUIYANG/sap-bah-openapi-backend-openclaw) <br>
- [Publisher profile](https://clawhub.ai/user/SHENRUIYANG) <br>
- [Quickstart](references/quickstart.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, generated files, and optional JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads OpenAPI JSON/YAML and OData EDMX files, can import downloaded specs, and can scaffold backend code from OpenAPI input.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
