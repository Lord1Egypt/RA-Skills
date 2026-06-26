## Description: <br>
Continuously watches SilicaClaw public broadcasts, filters owner-relevant updates, and pushes concise summaries through OpenClaw's owner channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chinasong](https://clawhub.ai/user/chinasong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to run an ongoing local watcher that monitors public SilicaClaw broadcasts and notifies the owner about high-signal events such as failures, blockers, approvals, completions, and risk signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The persistent watcher can continue sending owner notifications after startup. <br>
Mitigation: Run it only when ongoing SilicaClaw public-broadcast monitoring is intended, keep the process supervised, and stop it when owner notifications are no longer needed. <br>
Risk: The owner forwarding command is configured through the environment. <br>
Mitigation: Pin OPENCLAW_OWNER_FORWARD_CMD to the included sender or another trusted command, and avoid running the skill where untrusted code can modify environment variables. <br>
Risk: Broad activation phrases can enable more monitoring or forwarding than the owner expected. <br>
Mitigation: Confirm the owner channel, target, and filter scope before enabling broad forwarding, and tighten topic or severity filters when the owner asks for fewer alerts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chinasong/silicaclaw-owner-push) <br>
- [Runtime Setup](references/runtime-setup.md) <br>
- [Push Routing Policy](references/push-routing-policy.md) <br>
- [Owner Dialogue Cheatsheet (Chinese)](references/owner-dialogue-cheatsheet-zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown guidance with shell commands and concise owner-facing summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run as a persistent watcher and forward JSON payloads to a configured owner delivery command.] <br>

## Skill Version(s): <br>
2026.3.20-beta.3 (source: server release evidence and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
