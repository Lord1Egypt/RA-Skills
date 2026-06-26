## Description: <br>
Remote WeChat Official Account publishing skill that uses HTTP MCP to support stable publishing from changing home broadband IPs with isolated credentials and dependency checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MISAKIGA](https://clawhub.ai/user/MISAKIGA) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to publish Markdown articles to a WeChat Official Account draft box through a configured remote wenyan-mcp service, especially when the local network IP changes frequently. It also provides setup and troubleshooting guidance for credentials, MCP configuration, themes, and publishing scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WeChat AppID/AppSecret and unpublished article content are sent to the configured remote MCP server. <br>
Mitigation: Use only a server you control or fully trust, prefer HTTPS with authentication, and confirm that transmitting credentials and drafts to that server is acceptable. <br>
Risk: Credential storage and loading guidance is inconsistent across artifact files, including an older TOOLS.md path. <br>
Mitigation: Keep credentials in the dedicated wechat.env file with restrictive permissions, keep it out of version control, avoid the TOOLS.md credential path, and rotate credentials if exposure is possible. <br>
Risk: Publishing depends on remote server configuration, including WeChat IP allowlisting and remote wenyan-cli behavior. <br>
Mitigation: Whitelist the remote MCP server public IP, keep remote dependencies current, and test drafts before relying on publication workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MISAKIGA/wechat-mp-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/MISAKIGA) <br>
- [wenyan-mcp](https://github.com/caol64/wenyan-mcp) <br>
- [wenyan-cli](https://github.com/caol64/wenyan-cli) <br>
- [wenyan-cli theme assets](https://github.com/caol64/wenyan-core/tree/main/src/assets/themes) <br>
- [themes.md](references/themes.md) <br>
- [troubleshooting.md](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown instructions with bash, JSON, and article frontmatter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call local scripts that upload article content and WeChat credentials to the configured remote MCP server.] <br>

## Skill Version(s): <br>
2.0.2 (source: server-resolved release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
