## Description: <br>
S2-SP-OS Energy Radar maps household device inventory and generates local bar and trend dashboards for energy insights without cloud analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpaceSQ](https://clawhub.ai/user/SpaceSQ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inventory household energy devices, generate local dashboard charts, and surface energy-efficiency insights without sending analytics to cloud services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated dashboards can mislead users because the skill uses simulated household data unless real telemetry provenance is added. <br>
Mitigation: Label dashboards as demo or simulated data unless the deployment provides validated telemetry provenance. <br>
Risk: Energy insights may nudge agents toward unsafe power-control or HVAC automations. <br>
Mitigation: Require explicit per-device approval, safety exclusions, and a reversible confirmation flow before any connected smart-home skill changes power or HVAC state. <br>
Risk: The security verdict recommends review before installation. <br>
Mitigation: Review and scan the skill before deployment, and keep it limited to passive monitoring unless additional controls are approved. <br>


## Reference(s): <br>
- [S2-SP-OS Homepage](https://space2.world/s2-sp-os) <br>
- [ClawHub Skill Page](https://clawhub.ai/SpaceSQ/s2-energy-perception) <br>
- [S2 Energy Edge & Hardware Setup Guide](artifact/setup-guide.md) <br>
- [S2 Energy Memzero Protocol](artifact/S2-MEMZERO-PROTOCOL.md) <br>
- [Agent Reasoning Examples](artifact/AGENT-EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Markdown, Shell commands, Guidance] <br>
**Output Format:** [JSON status payloads with local file URI references to generated PNG dashboard charts, intended for Markdown presentation by the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and S2_PRIVACY_CONSENT=1; dashboard generation requires pandas, numpy, and matplotlib.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
