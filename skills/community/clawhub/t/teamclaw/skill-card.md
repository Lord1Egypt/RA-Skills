## Description: <br>
A high-performance Agent subsystem for complex multi-agent orchestration. It provides a visual workflow canvas (OASIS) to coordinate OpenClaw agents, automated computer use tasks, and real-time monitoring via a dedicated Web UI. Supports Telegram/QQ bot integrations and Cloudflare Tunnel for secure remote access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Avalon-467](https://clawhub.ai/user/Avalon-467) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use TeamClaw to run a local multi-agent orchestration service with an OpenAI-compatible chat API, OASIS workflow canvas, scheduled tasks, monitoring, bot integrations, and optional remote access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose broad local agent, file, command, network, persistent-memory, bot, and public-web controls. <br>
Mitigation: Install only in an environment where those capabilities are expected, review configuration before launch, and restrict access to trusted users. <br>
Risk: Optional Cloudflare Tunnel exposure can make the web UI reachable outside the local machine. <br>
Mitigation: Leave the tunnel disabled unless remote access is required, and add strong authentication and access controls before enabling it. <br>
Risk: This version passes and stores raw user passwords internally. <br>
Mitigation: Use dedicated, non-reused passwords for TeamClaw accounts and avoid sharing credentials across important services. <br>
Risk: Telegram and QQ bot integrations can receive commands from external messaging platforms. <br>
Mitigation: Configure bot tokens and allowlists carefully, and keep bot integrations disabled when they are not needed. <br>


## Reference(s): <br>
- [TeamClaw ClawHub release](https://clawhub.ai/Avalon-467/teamclaw) <br>
- [Publisher profile](https://clawhub.ai/user/Avalon-467) <br>
- [TeamClaw GitHub repository](https://github.com/Avalon-467/Teamclaw) <br>
- [OASIS external usage guide](artifact/OASIS_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, YAML workflow definitions, JSON API payloads, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include long-running background workflows, local API responses, scheduled-task status, bot messages, and web UI state.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata; artifact frontmatter metadata.version is 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
