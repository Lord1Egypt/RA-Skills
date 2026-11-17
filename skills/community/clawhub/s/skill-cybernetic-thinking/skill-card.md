## Description:

Thinking-mode skill for LLMs that applies control-theoretic and systems-theoretic reasoning to architecture, complex coding, coupled refactors, and non-deterministic debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shrimpleon](https://clawhub.ai/user/shrimpleon)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to guide agents through state identification, observability, stability checks, bounded intervention, and closed-loop verification before making non-trivial code or architecture changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer use can modify global, project-local, or shared cross-agent skill folders, and forced installs can replace an existing installation.

Mitigation: Install only from a trusted source, prefer a pinned command such as npx skill-cybernetic-thinking@0.6.0 install, review target locations before confirming, and use --force only when replacement is intended.

Risk: A broad thinking scaffold can encourage unnecessary analysis or an unsuitable control-theory framing for simple tasks.

Mitigation: Use it for non-trivial architecture, debugging, refactoring, and robustness work, and verify outcomes with tests, logs, metrics, or other observable checks.

## Reference(s):

- [Closed-Loop Workflow & Analysis-before-Synthesis](references/closed-loop-workflow.md)
- [State, Control, Observability & Bounds](references/state-and-control.md)
- [Stability](references/stability.md)
- [Modeling & Engineering Approximation](references/modeling.md)
- [Multivariable - Decouple What Hurts, Coordinate What Helps](references/multivariable.md)
- [Disturbance Compensation & Time-Delay](references/disturbance.md)
- [Time-Optimal & Bounded Control](references/bounded-control.md)
- [Discrete / Sampled Systems & Test Cadence](references/discrete-systems.md)
- [Possibility Space & Conjugate Control](references/possibility-space.md)
- [Black-Box Epistemology](references/black-box-epistemology.md)
- [Information and Control - The Mutual Dependence](references/information-and-control.md)
- [System Evolution - Stable States, Ultra-Stability, Catastrophe](references/system-evolution.md)
- [Original Text - Engineering Cybernetics](references/original-text.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown and plain text with prompt blocks, checklists, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API calls or external services are required by the skill itself.]

## Skill Version(s):

0.6.0 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
