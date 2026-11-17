## Description:

SynOmega Skill helps agents use the local synomega Python package for retrosynthesis, reaction prediction, multi-step synthesis planning, synthesizability scoring, plausibility screening, and multi-component reaction evolution for organic molecules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zbc0315](https://clawhub.ai/user/zbc0315)

### License/Terms of Use:

MIT

## Use Case:

Developers, chemists, and cheminformatics practitioners use this skill to ask an agent for synthesis planning, reaction outcome prediction, route scoring, and local command guidance around organic small molecules. It is intended for benign chemistry workflows and defers hazardous or controlled-compound decisions to the host safety policy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manual installation commands in the artifact can fetch executable code from mutable remote URLs without integrity checks.

Mitigation: Use the ClawHub install path; if installing manually, pin a reviewed commit and verify the provided file hashes before use.

Risk: The Python dependency and first-use model or stock downloads can affect privacy-sensitive, bandwidth-limited, air-gapped, or reproducibility-critical environments.

Mitigation: Run the dependency in a dedicated environment, pin requirements, and pre-fetch or mirror model assets before deployment.

Risk: Retrosynthesis and route-planning outputs can be dual-use for hazardous, controlled, or otherwise high-risk compounds.

Mitigation: Apply the host safety policy before giving operational synthesis guidance and require additional review for high-risk targets.

## Reference(s):

- [SynOmega documentation](https://zbc0315.github.io/synomega/)
- [SynOmega package on PyPI](https://pypi.org/project/synomega/)
- [Synomega Skill on ClawHub](https://clawhub.ai/zbc0315/skills/synomega)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON-producing helper commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper script prints JSON for retrosynthesis, forward prediction, planning, scoring, and multi-component evolution operations.]

## Skill Version(s):

1.8.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
