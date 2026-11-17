## Description:

Designs and manages multi-step VMware workflows with human approval gates and explicit, best-effort rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use Pilot to design, review, and coordinate multi-step VMware changes across companion skills, with approval gates and explicit best-effort rollback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented network setup may make infrastructure and security changes before approval, and the scan is incomplete because one referenced path could not be resolved.

Mitigation: Review the approval ordering and installation source before production use, and resolve the missing referenced path.

## Reference(s):

- [VMware Pilot on ClawHub](https://clawhub.ai/zw008/skills/vmware-pilot)
- [VMware Pilot project](https://github.com/vmware-skills/VMware-Pilot)
- [Workflow design guide](artifact/references/workflow-design.md)
- [Integration patterns](artifact/references/integration-patterns.md)
- [Workflow templates](artifact/references/templates.md)
- [Setup guide](artifact/references/setup-guide.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)
- [Model fit self-test guide](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands]

**Output Format:** [Markdown guidance with structured workflow details and YAML template examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe multi-step VMware actions that require human approval; rollback is explicit and best-effort.]

## Skill Version(s):

2.5.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
