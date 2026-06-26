## Description: <br>
Analyze home energy usage and propose safe, read-only automation plans for savings. Use when a user wants Home Assistant energy insights, optimization ideas, or draft automation YAML without directly controlling devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Home Assistant users, smart home operators, and developers use this skill to review energy usage, identify savings opportunities, and draft read-only automation plans for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Home Assistant tokens or home-identifying device details could be exposed during analysis. <br>
Mitigation: Use exported data or least-privilege read-only tokens, avoid admin credentials, keep tokens out of plain text files, and avoid sharing home addresses or uniquely identifying device details. <br>
Risk: Generated automation YAML could create comfort, safety, or accessibility issues if enabled without review. <br>
Mitigation: Manually review generated YAML before enabling it, exclude medical devices, security systems, and critical appliances, and preserve user comfort and safety constraints. <br>
Risk: Webhook or sensor inputs could contain invalid device identifiers, unexpected ranges, or noisy updates. <br>
Mitigation: Validate webhook sources, device IDs, and data ranges before using them, and rate limit processing to avoid spikes. <br>


## Reference(s): <br>
- [Overview](references/overview.md) <br>
- [Auth](references/auth.md) <br>
- [Endpoints](references/endpoints.md) <br>
- [Safety](references/safety.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [UX](references/ux.md) <br>
- [Webhooks](references/webhooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with Home Assistant YAML snippets, explanations, assumptions, and rollout checklist items.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft outputs only; the skill does not control devices or apply configuration changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
