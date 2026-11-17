## Description:

Provides guidance for IBM Rational Software Architect Designer (RSAD/RSA) use in IBM Financial Transaction Manager development, including UML and FSM modeling, Service Participant and Channel design, mapping design, and SQL export planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shoaibkhan](https://clawhub.ai/user/shoaibkhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design IBM FTM interfaces in RSAD, including UML diagrams, finite state machines, Service Participant and Channel models, mapping decisions, and SQL configuration exports. It is intended for RSAD/RSA design-time workflows before ACE build, deployment, and operational handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated RSAD, UML, FSM, or SQL export guidance could be incorrect for a specific IBM FTM environment.

Mitigation: Require normal human review and validate exported SQL against the DB2 schema before applying changes.

Risk: The broad trigger phrase may activate the skill outside RSAD and FTM design tasks.

Mitigation: Keep use limited to RSAD, UML, FSM, FTM interface design, and related SQL export planning.

Risk: Design recommendations may affect downstream ACE implementation work or version-control pull requests.

Mitigation: Review proposed design artifacts and PR content with the project team before committing or merging.

## Reference(s):

- [UML Modeling in RSAD](references/uml-modeling.md)
- [FTM Design Workflow in RSAD](references/ftm-design-workflow.md)
- [FSM Design in RSAD](references/fsm-design.md)
- [Mapping Design in RSAD](references/mapping-design.md)
- [FTM Patterns and RSAD Artifacts](references/patterns-artifacts.md)
- [Author GitHub profile](https://github.com/ShoaibKhan)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with tables, checklists, command or code snippets, UML/FSM design guidance, and SQL/configuration planning notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; generated SQL and design changes should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
