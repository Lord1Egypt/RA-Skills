## Description: <br>
Evaluate and QA a skill before release on ClawHub, skills.sh, and similar directories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fwwdn](https://clawhub.ai/user/fwwdn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to evaluate agent skills before release, compare versions, identify trigger and quality gaps, and generate structured readiness reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may activate the skill for general skill publication-readiness requests. <br>
Mitigation: Invoke it deliberately for skill QA tasks and confirm the target skill folder before evaluating. <br>
Risk: Static analysis can identify release-readiness issues but does not prove runtime correctness. <br>
Mitigation: Use deterministic or LLM-assisted grading only with an explicit test setup, and review unfamiliar target scripts before executing runtime tests. <br>


## Reference(s): <br>
- [Skill Test Listing](https://clawhub.ai/fwwdn/skills-test) <br>
- [Evaluation Methodology](references/eval-methodology.md) <br>
- [Grader Patterns](references/grader-patterns.md) <br>
- [Sandbox Testing](references/sandbox-testing.md) <br>
- [Comparison Workflow](references/comparison-workflow.md) <br>
- [Publish Evaluation](references/publish-evaluation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports with optional YAML, JSON, Python, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can propose eval.yaml suites and static evaluation commands; runtime and LLM grading evidence depends on user-provided test setup.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
