## Description:

A thermodynamic physics engine for BAS that equips agents with SSSU spatial mapping, thermal calibration, Causal Lookahead Control prediction, and dual-track authorization guidance.

This skill is for research and development only.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and building automation engineers use this skill to let an OpenClaw agent model BAS topology, calibrate thermal behavior, and produce advisory CLC decisions for HVAC scenarios. Security evidence limits this release to review, simulation, or documentation experiments until the authorization and actuation controls are completed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill concerns high-impact building HVAC control, and the authoritative security evidence says the shipped safety and authorization implementation is incomplete and not reliable.

Mitigation: Use it only for review, simulation, or documentation experiments; do not connect it to real building controls until hardware actuation is separately gated and signed short-lived BMS or homeowner tokens are verified outside the plugin.

Risk: Agent outputs may propose L2/L3 interventions that affect physical equipment.

Mitigation: Treat L2/L3 outputs as proposals requiring BMS approval in commercial spaces or homeowner authorization in residential spaces before any physical action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-bas-causal-os)
- [README](artifact/README.md)
- [S2-BAS-Causal-OS deployment use cases](artifact/s2-bas-causal-os-use-cases.md)
- [Building automation causal decision whitepaper](artifact/s2-bas-causal-decision-en.md)
- [Taohuayuan spatial causality whitepaper](artifact/s2-swm-spatial-causality-en.md)

## Skill Output:

**Output Type(s):** [text, json, code, configuration, guidance]

**Output Format:** [Markdown guidance and JSON-like tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool actions cover topology generation, physics calibration, and CLC prediction; L2/L3 physical interventions must remain externally authorized proposals.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
