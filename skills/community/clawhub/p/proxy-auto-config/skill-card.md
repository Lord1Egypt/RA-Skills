## Description: <br>
Automatically detects local proxy settings and configures OpenClaw Gateway environment variables, startup scripts, and recurring checks for common proxy tools such as v2ray, Clash, and Shadowsocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rutianze](https://clawhub.ai/user/rutianze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to detect available local proxy services and configure OpenClaw Gateway to run through them in restricted or proxied network environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make persistent networking changes by creating recurring proxy checks and local Gateway proxy configuration. <br>
Mitigation: Install only when persistent OpenClaw proxy management is intended, and review or patch the cron and systemd setup before running the installer. <br>
Risk: Proxy URLs may expose credentials if sensitive values are written into generated configuration files, logs, shell scripts, or service definitions. <br>
Mitigation: Avoid proxy URLs containing credentials and inspect generated files under the OpenClaw configuration directory before sharing logs or configuration. <br>
Risk: The security guidance identifies NODE_TLS_REJECT_UNAUTHORIZED=0 behavior, which disables normal Node.js HTTPS certificate validation. <br>
Mitigation: Remove or patch that behavior before use so HTTPS certificate validation remains enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rutianze/proxy-auto-config) <br>
- [Publisher profile](https://clawhub.ai/user/rutianze) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local proxy configuration, startup scripts, logs, cron entries, and systemd user service files when its scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
