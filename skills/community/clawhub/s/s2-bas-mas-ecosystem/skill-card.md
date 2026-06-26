## Description: <br>
Multi-Agent System for Building Automation powered by S2-SWM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
Space2 Custom License Agreement (S2-CLA) <br>


## Use Case: <br>
Facility engineers, building-automation developers, and energy operations teams use this skill to reason about local BAS, HVAC, microgrid, identity, and energy-audit workflows in a sandboxed multi-agent setup. It helps produce optimization proposals, dispatch guidance, audit summaries, and configuration steps for review before any real building-control deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill asks for sensitive building-control signing authority and describes high-impact automation without enough boundaries. <br>
Mitigation: Install only in a test or tightly controlled BAS sandbox, and add explicit human approval, least-privilege key management, audit logging, and safety limits before connecting it to production controls. <br>
Risk: The security guidance warns against providing production building-control keys, live actuator access, employee biometric data, EV/account data, or purchase authority without extra controls. <br>
Mitigation: Use non-production credentials and simulated data by default; require privacy, consent, spending-limit, and change-control reviews before enabling sensitive data or purchase-capable workflows. <br>
Risk: The artifact declares a required S2_BMS_MASTER_KEY and local governance file writes for PKI and building-sovereignty records. <br>
Mitigation: Store the key in an approved secret manager, restrict filesystem access to the declared governance path, rotate keys when testing is complete, and review generated ledger or key files before reuse. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spacesq/s2-bas-mas-ecosystem) <br>
- [S2-BAS-MAS Whitepaper (English)](docs/S2-BAS-MAS-Whitepaper-EN.md) <br>
- [S2-BAS-MAS Whitepaper (Chinese)](docs/S2-BAS-MAS-Whitepaper-CN.md) <br>
- [Release changelog](CHANGELOG.md) <br>
- [License terms](LICENSE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON-style proposals, Python code references, and shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require S2_BMS_MASTER_KEY and may write local governance, ledger, and key files when associated code is run.] <br>

## Skill Version(s): <br>
2.0.6 (source: SKILL.md frontmatter, CHANGELOG, and server evidence; package.json reports 2.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
