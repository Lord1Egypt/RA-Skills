## Description:

Provides a Python script intended to identify Western Blot gel bands, calculate band intensity, and report relative expression values against a control lane.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyla0921](https://clawhub.ai/user/lyla0921)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and lab analysts can use this skill as a starting point for Western Blot densitometry workflows and demo relative-expression calculations. Quantification results should be validated against known datasets before scientific use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation claims real Western Blot image analysis, but security review says the shipped code does not implement the described analysis of provided images.

Mitigation: Treat results as non-authoritative until the implementation and documentation are corrected and validated against known Western Blot datasets.

Risk: The skill runs local Python with scientific-image dependencies and local file input/output.

Mitigation: Install in an isolated environment, pin and review dependencies, and check input and output paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lyla0921/skills/western-blot-quantifier)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python and bash examples; script output includes console text and CSV-style quantified band tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local image paths and may write result files; current evidence indicates real-image quantification should be validated before use.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
