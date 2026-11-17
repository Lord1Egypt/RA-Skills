## Description:

Truth Tutor is a diagnosis-first learning coach that identifies why a learner is stuck and returns evidence-based learning gaps, direct feedback, and actionable drills across general, paper-reading, and alphaXiv recovery modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sii-k7](https://clawhub.ai/user/sii-k7)

### License/Terms of Use:

MIT-0

## Use Case:

External learners use this skill when they need diagnosis-first tutoring for a concept, research paper, or failed alphaXiv explanation. It helps identify the root learning gap, choose the right reread or repair path, and produce verification drills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blunt coaching feedback may feel too sharp for users who want gentle tutoring or simple explanations.

Mitigation: Respect the skill's safety boundary: keep criticism attached to the work, avoid identity attacks, and avoid harsh modes when the user appears to be in emotional crisis.

Risk: A diagnosis made from thin context may misidentify the learner's actual gap.

Mitigation: Collect the minimum context when possible, label provisional diagnoses when context is incomplete, and include verification drills so the learner can test whether the diagnosis fits.

## Reference(s):

- [Gap Taxonomy](references/gap-taxonomy.md)
- [Response Template](references/response-template.md)
- [Paper Reading Mode](references/paper-reading-mode.md)
- [alphaXiv Intake Mode](references/alphaxiv-intake.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown learning diagnosis with ranked gaps, recovery plan, and drills]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tone varies by requested strictness level while keeping critique attached to the work rather than the learner's identity.]

## Skill Version(s):

1.0.9 (source: server release evidence; artifact frontmatter says 1.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
