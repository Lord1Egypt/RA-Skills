## Description:

Evaluate and QA agent skills before release with a bundled static evaluator plus guidance for deterministic or LLM-assisted grading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fwwdn](https://clawhub.ai/user/fwwdn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to evaluate agent skills before adoption, publication, or version comparison. It helps check trigger quality, structure, release blockers, regression risk, and readiness evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime tests against unfamiliar or side-effectful skills may expose the user to unintended local actions.

Mitigation: Review the target skill before runtime testing and use an isolated workspace or disposable session for unfamiliar skills.

Risk: Scaffold mode can create or replace eval.yaml in the target skill directory.

Mitigation: Use --scaffold only when creating or replacing eval.yaml is intended, and review existing files before running it.

Risk: Static analysis does not prove runtime correctness or publish readiness for skills that depend on external systems.

Mitigation: Treat static evaluator results as a baseline and add deterministic, runtime, or manual verification when external behavior matters.

## Reference(s):

- [Skill Test listing](https://clawhub.ai/fwwdn/skills/skills-test)
- [Evaluation Methodology](references/eval-methodology.md)
- [Grader Patterns](references/grader-patterns.md)
- [Sandbox Testing](references/sandbox-testing.md)
- [Comparison Workflow](references/comparison-workflow.md)
- [Publish Evaluation](references/publish-evaluation.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with optional JSON evaluator output and YAML eval-suite configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled evaluator can emit text or JSON reports; optional scaffold mode can create eval.yaml for regression tests.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
