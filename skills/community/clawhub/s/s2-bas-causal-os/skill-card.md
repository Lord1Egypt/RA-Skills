## Description: <br>
A thermodynamic physics engine for BAS that equips agents with SSSU spatial mapping, thermal calibration, and Causal Lookahead Control (CLC) prediction with dual-track authorization for commercial and residential safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, BAS engineers, and building-automation operators use this skill to model smart-space topology, calibrate thermal behavior, and generate Causal Lookahead Control recommendations for HVAC operation. L2 and L3 hardware-affecting decisions should be treated as proposals unless an external BMS or owner-token authorization system approves execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes HVAC setpoint overrides, fan locks, and FCU shutdowns that could affect live building systems. <br>
Mitigation: Use only in simulation or carefully controlled BAS testing unless external BMS or owner-token approvals, manual overrides, audit logs, safety limits, shutdown behavior, setpoint overrides, and fan locks are implemented and tested. <br>
Risk: CLC decisions can propose L2 or L3 hardware-affecting actions based on predicted thermodynamic risk. <br>
Mitigation: Treat hardware-affecting outputs as proposal-only until a BMS dispatch token or owner digital ID authorizes execution for the target space. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spacesq/s2-bas-causal-os) <br>
- [Publisher profile](https://clawhub.ai/user/spacesq) <br>
- [README](artifact/README.md) <br>
- [Building Automation Causal Decision Whitepaper](artifact/s2-bas-causal-decision-en.md) <br>
- [Spatial Causality and Element Supply Source Axiom System](artifact/s2-swm-spatial-causality-en.md) <br>
- [Deployment Use Cases](artifact/s2-bas-causal-os-use-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance, Configuration] <br>
**Output Format:** [JSON tool responses and concise agent-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include topology, calibration, and CLC decision information; hardware-affecting recommendations require external authorization before live actuation.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
