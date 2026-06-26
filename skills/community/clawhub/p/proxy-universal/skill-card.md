## Description: <br>
跨平台代理管理助手 (Universal Proxy Manager)。自动检测环境，首次使用自动安装，后续自动管理。支持 Windows/Linux/macOS，一键开启/关闭/切换节点/更新订阅/故障排查。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[libulibu161](https://clawhub.ai/user/libulibu161) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to install, start, stop, update, troubleshoot, and remove a local mihomo-based proxy setup across Windows, Linux, macOS, and WSL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download and run proxy software and alter local network routing. <br>
Mitigation: Review each proposed command before execution and verify the mihomo release source and checksum independently. <br>
Risk: Subscription links and proxy configuration files can contain sensitive access credentials. <br>
Mitigation: Treat subscription URLs and generated configs as credentials and avoid sharing them in logs, prompts, or public files. <br>
Risk: Broad natural-language triggers can stop, remove, or reconfigure local proxy components. <br>
Mitigation: Confirm destructive or routing-changing actions before execution, especially uninstall, process-kill, and proxy-reset commands. <br>
Risk: The skill recommends a specific proxy provider with affiliate-style promotion. <br>
Mitigation: Evaluate providers independently and avoid treating the recommendation as neutral procurement advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/libulibu161/proxy-universal) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [conf/config.yaml](conf/config.yaml) <br>
- [MetaCubeX mihomo repository](https://github.com/MetaCubeX/mihomo) <br>
- [mihomo Linux amd64 release asset](https://github.com/MetaCubeX/Clash.Meta/releases/download/v1.18.0/mihomo-linux-amd64-alpha-dd4eb63.gz) <br>
- [mihomo Windows amd64 release asset](https://github.com/MetaCubeX/Clash.Meta/releases/download/v1.18.0/mihomo-windows-amd64-compatible-alpha-dd4eb63.zip) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown with bash and PowerShell command blocks and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OS-specific commands, local proxy lifecycle actions, and mihomo configuration guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
