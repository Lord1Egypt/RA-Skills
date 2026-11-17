## Description:

Guides agents through writing and updating trusted software specification files, coverage metadata, and impact reports without inventing unconfirmed requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jivecheng](https://clawhub.ai/user/jivecheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product or engineering teams use this skill to maintain structured software specs, requirements, ADRs, acceptance criteria, and spec coverage metadata while keeping unconfirmed decisions explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can pause feature implementation when functional requirements or acceptance criteria are missing.

Mitigation: Maintain spec coverage metadata and add draft or confirmed FR and AC entries before coding the affected feature.

Risk: Unconfirmed requirements could be written as if they were settled project decisions.

Mitigation: Keep uncertain items in coverage metadata as draft, tbd, or missing, and write only confirmed information into specification files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jivecheng/skills/software-spec-writing)
- [Chapters Reference](references/chapters.md)
- [Writing Conventions](references/conventions.md)
- [Coverage Schema](references/coverage.md)
- [Glossary](references/glossary.md)
- [Spec Coverage Template](assets/spec-coverage.template.yaml)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance]

**Output Format:** [Markdown and YAML guidance for specification files and coverage metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May pause feature implementation when functional requirements and acceptance criteria are missing.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
