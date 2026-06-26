## Description: <br>
Token Burn Monitor provides a local OpenClaw dashboard for tracking per-agent token usage, model cost breakdowns, cache hit rates, cron health, and 30-day trends, with prompts redacted by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KasparChen](https://clawhub.ai/user/KasparChen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to monitor daily token burn, model cost, cache efficiency, per-call details, and cron job health from local session and cron data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard reads local OpenClaw session logs and cron data. <br>
Mitigation: Install it only on machines where the dashboard is permitted to read those files. <br>
Risk: Prompt text can become visible when prompt display is explicitly enabled. <br>
Mitigation: Keep showPrompts and SHOW_PROMPTS disabled unless every dashboard viewer is trusted to see prompt text. <br>
Risk: Custom themes can display any data returned by the local API. <br>
Mitigation: Review custom or third-party themes before enabling them. <br>
Risk: Exposing the service beyond localhost could reveal local usage and cost data. <br>
Mitigation: Keep the server bound to localhost unless a separate access-control layer is reviewed and approved. <br>


## Reference(s): <br>
- [Token Burn Monitor API Reference](API.md) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [ClawHub listing](https://clawhub.ai/KasparChen/token-burn-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown setup guidance, shell commands, JSON API responses, and local dashboard views] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs as a localhost Node.js service and reads OpenClaw session and cron files.] <br>

## Skill Version(s): <br>
5.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
