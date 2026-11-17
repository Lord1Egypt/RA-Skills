## Description:

Automates Siemens TIA Portal Openness workflows for PLC project creation, hardware configuration, SCL block generation, compilation, and download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiansiting](https://clawhub.ai/user/jiansiting)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to create TIA Portal projects, configure S7-1200/1500 PLC hardware, generate SCL program blocks, compile PLC software, and optionally download changes to a target PLC.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Download and full_automation actions can make production-impacting changes to real PLC controllers.

Mitigation: Use only in authorized engineering environments and require explicit approval before running PLC download workflows.

Risk: Generated SCL, compile diagnostics, project target, interface, or IP address may be incorrect for the intended controller.

Mitigation: Review generated SCL, compile results, target PLC name, interface, IP address, and change authorization before execution.

Risk: The artifact does not include a pinned dependency lockfile.

Mitigation: Pin and review dependencies before using the skill near real equipment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiansiting/skills/tia-openness-complete-skill)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact readme](artifact/readme.txt)

## Skill Output:

**Output Type(s):** [JSON, Code, Configuration, Guidance]

**Output Format:** [JSON status objects plus generated SCL and TIA Portal project changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Windows, Siemens TIA Portal Openness, pythonnet, and jinja2; download and full automation actions may affect real PLC targets.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
