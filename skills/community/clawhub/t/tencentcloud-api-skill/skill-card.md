## Description: <br>
Helps an agent use Tencent Cloud's tccli and Cloud API documentation to query, create, modify, and delete Tencent Cloud resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to plan and execute Tencent Cloud API operations through tccli, including resource discovery, configuration, and managed create/modify/delete workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help operate Tencent Cloud resources, including create, modify, and delete actions. <br>
Mitigation: Use least-privilege CAM permissions and review exact tccli commands before approving write operations. <br>
Risk: Credential handling is required for tccli authentication. <br>
Mitigation: Complete OAuth login directly in the browser and do not paste SecretId, SecretKey, or other cloud secrets into chat. <br>
Risk: API output is JSON data that could be misread or treated as executable content. <br>
Mitigation: Treat tccli responses as data for review and avoid executing content returned by cloud APIs. <br>


## Reference(s): <br>
- [Tencent Cloud API documentation index](https://cloudcache.tencentcs.com/capi/refs/services.md) <br>
- [Tencent Cloud CLI source and installation reference](https://github.com/TencentCloud/tencentcloud-cli.git) <br>
- [Credential configuration reference](references/auth.md) <br>
- [TCCLI installation reference](references/install.md) <br>
- [API reference lookup steps](references/refs.md) <br>
- [ClawHub skill page](https://clawhub.ai/tencent-adm/tencentcloud-api-skill) <br>
- [Publisher profile](https://clawhub.ai/user/tencent-adm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose tccli commands and interpret JSON API responses; write operations should be explicitly reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
