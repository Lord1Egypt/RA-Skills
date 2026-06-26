## Description: <br>
快速查询本机系统信息和OpenClaw配置。包括CPU、内存、磁盘、网络、环境配置、硬件资源占用、Docker容器、OpenClaw配置/频道/插件/服务状态。当用户询问"系统状态"、"CPU使用率"、"内存占用"、"磁盘空间"、"网络信息"、"硬件配置"、"进程状态"、"Docker状态"、"系统负载"、"配置信息"、"OpenClaw状态"时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evangeliona](https://clawhub.ai/user/evangeliona) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local system status and OpenClaw configuration when troubleshooting CPU, memory, disk, network, Docker, GPU, process, service, or OpenClaw runtime questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic output can reveal operational details such as hostnames, IP addresses, channel names, Docker state, and service status. <br>
Mitigation: Request only the needed module and review the output before sharing it outside the local troubleshooting context. <br>
Risk: Redacted OpenClaw configuration summaries may still expose configuration structure or non-secret identifiers. <br>
Mitigation: Treat OpenClaw output as environment-sensitive even when credentials are redacted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evangeliona/quick-sysinfo) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text diagnostic output, optionally summarized in Markdown by the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional module argument selects all, cpu, mem, disk, net, env, load, proc, gpu, docker, or openclaw.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
