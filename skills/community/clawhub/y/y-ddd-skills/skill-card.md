## Description:

Chinese-language DDD guidance suite for agents covering core concepts, architecture, tactical design, new-project setup, legacy refactoring, and DDD code review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renyangy](https://clawhub.ai/user/renyangy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and software architecture teams use this skill to guide domain-driven design work in Chinese, from strategic modeling through Java/Kotlin Spring/JPA implementation patterns and code review. It helps agents route requests to focused DDD subskills for concept explanation, architecture rules, tactical patterns, new project setup, refactoring, and review checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gradle examples may be copied into a real project without exact dependency version review.

Mitigation: Pin exact dependency versions and review generated build configuration before adoption.

Risk: Domain-event examples may be applied with incorrect transaction timing.

Mitigation: Review event-publishing code for correct after-commit transaction semantics before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/renyangy/skills/y-ddd-skills)
- [Gradle dependency guidance](ddd-architecture/references/gradle-dependencies.md)
- [Package structure guidance](ddd-architecture/references/package-structure.md)
- [DDD code review checklist](ddd-code-review/references/checklist.md)
- [Context mapping guide](ddd-core-concepts/references/context-mapping.md)
- [Ubiquitous language glossary](ddd-core-concepts/references/glossary.md)
- [Event storming workshop guide](ddd-new-project/references/event-storming.md)
- [Naming guidance](ddd-new-project/references/naming.md)
- [Project scaffolding guide](ddd-new-project/references/scaffolding.md)
- [Legacy system analysis guide](ddd-refactoring/references/legacy-analysis.md)
- [Refactoring patterns](ddd-refactoring/references/refactoring-patterns.md)
- [Aggregate design guidance](ddd-tactical-design/references/aggregate.md)
- [Domain event guidance](ddd-tactical-design/references/domain-event.md)
- [Entity design guidance](ddd-tactical-design/references/entity.md)
- [Repository guidance](ddd-tactical-design/references/repository.md)
- [Value object guidance](ddd-tactical-design/references/value-object.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown guidance with Java, Kotlin, Spring/JPA, and Gradle examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance; no tool calls or executable scripts are included in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
