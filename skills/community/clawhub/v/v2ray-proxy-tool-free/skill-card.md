## Description: <br>
网络连通性诊断工具免费版，面向个人开发者的轻量级网络排障工具，支持 ping/traceroute 连通性检测、端口开放性扫描、DNS 解析诊断和路由追踪分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to diagnose API timeouts, DNS resolution problems, closed ports, and route latency by having an agent propose or run common local network diagnostic commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local network probes such as ping, traceroute, DNS lookup, and port checks can be logged, blocked, or violate policy when run against systems without permission. <br>
Mitigation: Run diagnostics only against hosts and services you own or are authorized to test, and review proposed shell commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/v2ray-proxy-tool-free) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and structured diagnostic summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local network command output, status codes, execution logs, DNS results, port status, and route diagnostics.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
