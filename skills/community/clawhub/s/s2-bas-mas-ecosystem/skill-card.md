## Description:

Multi-Agent System for Building Automation powered by S2-SWM.

This skill is for research and development only.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

S2 Custom License Agreement (S2-CLA)

## Use Case:

Developers and building-automation engineers use this skill to evaluate a local simulated multi-agent building automation ecosystem for HVAC, hydronic distribution, ground-source heat pumps, microgrids, forecasting, identity registration, and energy auditing. It produces advisory proposals, reports, commands, and configuration guidance that require strict controls before any physical or financial deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for sensitive building-control authority while approval and safety boundaries are not strong enough for direct deployment.

Mitigation: Use it as research or simulation unless strict deployment controls are added, and require explicit human approval before physical control actions.

Risk: Master signing keys and private-key access could authorize unsafe or unintended subsystem actions.

Mitigation: Isolate the master signing key, remove private-key access from subsystem agents, and use hardened key management such as an HSM for production-like testing.

Risk: Dispatch authorization may be replayed or separated from important command context.

Mitigation: Sign complete command envelopes with timestamps, target identities, nonces, and replay protection before connecting to real systems.

Risk: Unpinned dependencies can change security and behavior across installs.

Mitigation: Pin dependencies, verify package hashes, and scan the environment before execution.

Risk: Occupancy, EV, and wearable-data scenarios can expose sensitive personal or operational data.

Mitigation: Define privacy controls, data minimization, consent, retention, and access policies before using those data types.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/spacesq/skills/s2-bas-mas-ecosystem)
- [S2-BAS-MAS Whitepaper EN](artifact/docs/S2-BAS-MAS-Whitepaper-EN.md)
- [S2-BAS-MAS Whitepaper CN](artifact/docs/S2-BAS-MAS-Whitepaper-CN.md)
- [Skill Directives](artifact/SKILL.md)
- [Release Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code, Python examples, JSON configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local simulation outputs can include signed dispatch tokens, advisory control proposals, energy and carbon reports, identity registry records, and visualization JSON.]

## Skill Version(s):

2.0.6 (source: SKILL.md frontmatter, ClawHub release evidence, CHANGELOG released 2026-04-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
