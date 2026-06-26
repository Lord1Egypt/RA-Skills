## Description: <br>
Per-agent feedback loop for OpenClaw that captures corrections, errors, and feature requests, detects repeated patterns per workspace, notifies through the bound channel bot, and supports A/B/C/D improvement actions in the corresponding agent session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[one2agi](https://clawhub.ai/user/one2agi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to maintain isolated self-improvement feedback loops across agent workspaces, review recurring corrections or failures, and turn approved patterns into skill or instruction updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes persistent changes to routing, cron jobs, agent instructions, and related skills. <br>
Mitigation: Review install.sh, scripts/agents-append.md, scripts/cron-payloads.json, and setup_crons.py before installation, and back up ~/.openclaw/openclaw.json plus agent workspaces first. <br>
Risk: Gateway API configuration can expose authorization tokens if pointed at an untrusted endpoint. <br>
Mitigation: Verify OPENCLAW_GATEWAY_URL points only to a trusted local gateway before exposing gateway authentication tokens. <br>
Risk: A/B/C/D bulk actions can create or modify skills and persistent agent instructions across workspaces. <br>
Mitigation: Use A/B/C/D actions only after reviewing the pending notifications and the target workspace; choose skip when the proposed change is not intended. <br>
Risk: Concurrent notifications may cause replies to route to the wrong agent session. <br>
Mitigation: Process pending notifications deliberately and verify the target agent workspace before accepting create, improve, or promote actions. <br>


## Reference(s): <br>
- [Setup Guide](references/setup-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/one2agi/self-improvement-loop) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, JSON pending-notification records, and shell or Python command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Per-agent output is scoped by the OpenClaw agent workspace and LEARNINGS_DIR.] <br>

## Skill Version(s): <br>
4.6.17 (source: server release metadata; artifact frontmatter reports 4.6.13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
