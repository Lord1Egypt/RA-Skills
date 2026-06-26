## Description: <br>
Track elapsed time from a set epoch with tamper-evident locking for uptime, service hours, time since events, sobriety counters, project duration, equipment runtime, and similar counters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rm289](https://clawhub.ai/user/rm289) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and operators use TARDIS to create, lock, check, verify, list, and export tamper-evident elapsed-time meters with optional milestone notifications and career projection calculations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Networked notification and webhook features can expose SendGrid events or forward them to configured Discord/OpenClaw destinations. <br>
Mitigation: Install those features only when needed, review what event data is sent, and enable SendGrid signature verification for webhook use. <br>
Risk: Broad environment loading can read more secrets than the meter needs. <br>
Mitigation: Use a dedicated least-privilege configuration for SendGrid and avoid broad .env loading for local-only use. <br>
Risk: Background webhook tunnels can make a local service publicly reachable. <br>
Mitigation: Do not run check-webhook-services.sh or Cloudflare/ngrok tunnels for local-only tracking, and review tunnel exposure before enabling webhooks. <br>
Risk: ACTION milestone triggers can become agent instructions if explicitly enabled. <br>
Mitigation: Keep ACTION triggers opt-in and restrict who can edit meters.json and HEARTBEAT.md. <br>


## Reference(s): <br>
- [ClawHub TARDIS Release](https://clawhub.ai/rm289/tardis) <br>
- [README](README.md) <br>
- [Technical Whitepaper](WHITEPAPER.md) <br>
- [Skill Definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local meter storage and witness files when the user runs the bundled commands.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
