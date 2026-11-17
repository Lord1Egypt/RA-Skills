## Description:

Create new skills, modify and improve existing skills, and measure skill performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luowanqian](https://clawhub.ai/user/luowanqian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create, revise, evaluate, benchmark, package, and tune agent skills through an iterative workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review and evaluation tooling opens local review HTML, may start a localhost server, and may terminate another local process using the chosen viewer port.

Mitigation: Prefer static review output for untrusted evaluations, check the viewer port before serving, and review generated pages before opening them.

Risk: Automation runs local evaluation scripts, calls the claude CLI, and writes temporary .claude command files.

Mitigation: Use the skill only in trusted workspaces, inspect generated prompts and files, and avoid running it on adversarial skill outputs without additional review.

## Reference(s):

- [Skill Creator on ClawHub](https://clawhub.ai/luowanqian/skills/skill-creator-3)
- [Evaluation and Benchmark Schemas](artifact/references/schemas.md)
- [Analyzer Agent Guide](artifact/agents/analyzer.md)
- [Comparator Agent Guide](artifact/agents/comparator.md)
- [Grader Agent Guide](artifact/agents/grader.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, inline shell commands, generated skill files, evaluation artifacts, and review reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local workspace files, packaged skill archives, benchmark summaries, and static or served HTML review pages.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
