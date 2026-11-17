## Description:

Tencent Cloud Object Storage (COS) and Data Wanxiang (CI) integration skill for managing cloud storage files, image processing, intelligent image search, document-to-PDF conversion, and video smart cover generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to configure Tencent Cloud COS access, perform object storage operations, and invoke COS/CI media-processing workflows from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup process handles Tencent Cloud credentials and may persist long-lived secrets in local shell startup files.

Mitigation: Use a dedicated least-privilege Tencent CAM key, avoid pasting broad credentials into chat, and prefer environment or secret-manager handling that does not store long-lived secrets in shell profile files.

Risk: Setup installs and runs local Node/Python tooling, including packages used for MCP, SDK, and optional COSCMD workflows.

Mitigation: Review the setup script before running it, pin or vet package versions where possible, and install only in an environment appropriate for cloud credential use.

Risk: Custom service domains or disabling HTTPS can change the trust boundary for COS API requests.

Mitigation: Keep HTTPS enabled and avoid custom service domains unless they are required and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jason-aka-chen/skills/tencent-cos-chen)
- [cos-mcp GitHub repository](https://github.com/Tencent/cos-mcp)
- [COS Node.js SDK documentation](https://www.tencentcloud.com/zh/document/product/436/8629)
- [COSCMD documentation](https://www.tencentcloud.com/zh/document/product/436/10976)
- [API reference](artifact/references/api_reference.md)
- [MCP configuration template](artifact/references/config_template.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration, code, JSON results]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce signed object URLs and local configuration changes when the user runs setup or storage commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
