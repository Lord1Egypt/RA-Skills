## Description: <br>
Captures smart-home automation conflicts, sensor drift, device connectivity failures, integration regressions, safety rule gaps, and energy optimization opportunities for continuous domotics improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, smart-home operators, and agent users use this skill to record domotics learnings, issues, and feature requests so recurring automation conflicts, sensor drift, connectivity failures, safety gaps, and energy opportunities can be reviewed and promoted into safer operating patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Domotics logs can expose sensitive household details such as lock PINs, alarm codes, tokens, Wi-Fi credentials, or occupancy schedules. <br>
Mitigation: Do not log secrets or private household schedules in plaintext; redact sensitive details before sharing logs or generated skills. <br>
Risk: Optional hook matchers can become too broad and create noisy or poorly scoped reminders. <br>
Mitigation: Keep hooks opt-in and narrow matchers to domotics-specific terms before enabling reminder automation. <br>
Risk: Generated skill scaffolds may contain incomplete TODOs or unsafe domotics assumptions if enabled without review. <br>
Mitigation: Review and scan generated skill scaffolds before enabling or sharing them, especially for routines involving locks, alarms, gas, water, or heaters. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/jose-compu/self-improving-house) <br>
- [Domotics Entry Examples](references/examples.md) <br>
- [Domotics Hook Setup Guide](references/hooks-setup.md) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and optional hook or scaffold code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or updates local markdown learning logs when the user applies the guidance; optional hooks are reminder-only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
