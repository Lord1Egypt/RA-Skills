## Description: <br>
Tencent Cloud Object Storage (COS) and Cloud Infinite (CI) integration skill for uploading, downloading, and managing cloud storage files, image processing, intelligent image search, document-to-PDF conversion, and video smart-cover generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Tencent Cloud COS access, manage bucket objects, and call COS and CI capabilities through MCP, Node.js SDK, or COSCMD fallback commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can persist powerful Tencent Cloud credentials in shell startup files, mcporter configuration, and COSCMD configuration. <br>
Mitigation: Use a dedicated least-privilege CAM key, prefer session-only environment variables or a secret manager, avoid shared machines for persistent setup, and rotate any key already written to local configuration files. <br>
Risk: The skill documents delete, recursive delete, copy, and move operations that can alter or remove bucket data. <br>
Mitigation: List the target prefix before destructive actions, require explicit confirmation for delete or recursive delete, and avoid delete-capable credentials unless the workflow needs them. <br>
Risk: Signed object URLs can grant temporary access to COS objects. <br>
Mitigation: Use short expirations, share signed URLs only with intended recipients, and avoid generating links for sensitive objects unless access is required. <br>


## Reference(s): <br>
- [Tencent Cloud COS operation reference](artifact/references/api_reference.md) <br>
- [Tencent Cloud COS MCP configuration template](artifact/references/config_template.json) <br>
- [cos-mcp GitHub repository](https://github.com/Tencent/cos-mcp) <br>
- [Tencent Cloud COS Node.js SDK documentation](https://www.tencentcloud.com/zh/document/product/436/8629) <br>
- [Tencent Cloud COSCMD documentation](https://www.tencentcloud.com/zh/document/product/436/10976) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Setup can create or update local MCP, shell environment, and COSCMD configuration files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
