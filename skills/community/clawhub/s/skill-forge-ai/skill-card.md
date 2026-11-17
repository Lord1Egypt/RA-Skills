## Description:

Skill Forge helps developers create, evaluate, and improve agent skills through a gated interview, peer-check, validation, and handoff workflow, with a separate assessment path for SkillHub comparison and Tencent nine-dimension scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to turn repeatable workflows into agent skills, evaluate existing skills, and improve existing skills through a diagnosis-and-confirmation path before publication handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or modified skill files may contain inaccurate scope, unsafe permissions, or misleading instructions.

Mitigation: Review generated SKILL.md and reference files, then run the normal platform validation and scan steps before installation or publication.

Risk: Sensitive information provided during authoring could be summarized into reusable skill artifacts.

Mitigation: Do not provide secrets, credentials, private customer data, or unrelated sensitive material; redact inputs before using the skill.

Risk: The skill can modify existing skill files on the R5 improvement path.

Mitigation: Confirm the diagnosis and intended file changes before allowing edits, and keep publishing in the separate publisher workflow.

## Reference(s):

- [Skill Forge on ClawHub](https://clawhub.ai/edwardwason/skills/skill-forge-ai)
- [Project Homepage](https://github.com/EdwardWason/skill-forge)
- [Authoring Principles](references/authoring-principles.md)
- [Pre-Gate and Routing](references/pre-gate-and-routing.md)
- [Interview Flow](references/interview-flow.md)
- [Composition and Pipeline](references/composition-and-pipeline.md)
- [Interview Methods](references/interview-methods.md)
- [Benchmarking Guide](references/benchmarking-guide.md)
- [Meeting Action Extractor Example](references/meeting-action-extractor-example.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated or modified skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or edit SKILL.md, reference files, scripts, or assets after user confirmation; publishing is out of scope.]

## Skill Version(s):

6.4.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
