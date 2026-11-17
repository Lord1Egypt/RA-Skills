## Description:

Reliable SAP Business Accelerator Hub API spec downloader for OpenClaw that uses SAP_HUB_USERNAME and SAP_HUB_PASSWORD with Playwright Chromium to download OpenAPI JSON/YAML and OData EDMX files, validate payload signatures, and support importing specs into APIConnectionToSAP categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenruiyang](https://clawhub.ai/user/shenruiyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to authenticate to SAP Business Accelerator Hub, download API specification files, import those files into APIConnectionToSAP categories, and optionally scaffold backend code from trusted OpenAPI specs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SAP credentials are required at runtime and could be exposed to the local execution environment.

Mitigation: Run the skill only in a trusted local runtime, provide credentials through SAP_HUB_USERNAME and SAP_HUB_PASSWORD, and do not upload real credentials to ClawHub.

Risk: The default output directory is /usr/download, which may require elevated setup or write permissions.

Mitigation: Prefer a user-owned output directory with --output-dir, or explicitly create and assign permissions for /usr/download before running downloads.

Risk: The backend scaffolder is under-disclosed in the release summary and has security guidance around unsafe file-writing, code-string escaping, and path containment.

Mitigation: Use the scaffolder only with trusted OpenAPI files, review generated code before use, and avoid shared, CI, or production environments until the identified issues are fixed.

Risk: Runtime dependencies are not pinned to exact versions.

Mitigation: Pin and review dependencies before using this skill in shared, CI, or production environments.

## Reference(s):

- [Quickstart](artifact/references/quickstart.md)
- [ClawHub Skill Page](https://clawhub.ai/shenruiyang/skills/sap-bah-openapi-backend-openclaw)
- [Publisher Profile](https://clawhub.ai/user/shenruiyang)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus downloaded OpenAPI JSON/YAML, OData EDMX files, optional JSON reports, imported spec files, and generated Python backend modules.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output directory is /usr/download; the skill requires SAP_HUB_USERNAME and SAP_HUB_PASSWORD and supports linux and darwin runtimes.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
