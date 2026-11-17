## Description:

跨平台代理管理助手 (Universal Proxy Manager)。自动检测环境，首次使用自动安装，后续自动管理。支持 Windows/Linux/macOS，一键开启/关闭/切换节点/更新订阅/故障排查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[libulibu161](https://clawhub.ai/user/libulibu161)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to install, start, stop, update, troubleshoot, and manage a local mihomo-compatible proxy configuration across Windows, Linux, macOS, and WSL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs an unverified native proxy binary.

Mitigation: Verify downloaded binaries before execution and install only when the user accepts that trust boundary.

Risk: The skill starts long-running background network processes and stores proxy configuration under the user profile.

Mitigation: Ask before state-changing actions, document where local files and logs are stored, and provide a clear stop and uninstall path.

Risk: The skill can alter Windows proxy settings and may affect host networking beyond the current agent session.

Mitigation: Preserve previous proxy settings before changes and restore them when the proxy is stopped or uninstalled.

Risk: Operational instructions include affiliate steering for a proxy provider.

Mitigation: Remove affiliate recommendations from operational guidance or clearly separate them from required setup steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/libulibu161/skills/proxy-universal)
- [Artifact README](artifact/README.md)
- [mihomo official repository](https://github.com/MetaCubeX/mihomo)
- [Linux mihomo release artifact referenced by the skill](https://github.com/MetaCubeX/Clash.Meta/releases/download/v1.18.0/mihomo-linux-amd64-alpha-dd4eb63.gz)
- [Windows mihomo release artifact referenced by the skill](https://github.com/MetaCubeX/Clash.Meta/releases/download/v1.18.0/mihomo-windows-amd64-compatible-alpha-dd4eb63.zip)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local proxy setup and management, including configuration files, background process control, subscription updates, and troubleshooting steps.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
