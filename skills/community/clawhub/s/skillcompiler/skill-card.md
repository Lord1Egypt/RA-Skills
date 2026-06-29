## Description: <br>
Skill Compiler converts reusable prompts into structured AI skill packages with an IR-driven analyze, design, generate, optimize, and validate workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qomob](https://clawhub.ai/user/qomob) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this meta-skill to turn repeatable prompts into reusable AI skill packages with modular files, validation checks, platform profiles, and a compilation report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skills can include broad triggers or propose unsafe behavior when the source prompt is under-specified. <br>
Mitigation: Review generated skills before installation, especially for external tools, account actions, code execution, sensitive data, and trigger wording. <br>


## Reference(s): <br>
- [Skill Compiler README](README.md) <br>
- [Pass 1 Analyze](references/pass-1-analyze.md) <br>
- [Pass 2 Extract](references/pass-2-extract.md) <br>
- [Pass 3 Design](references/pass-3-design.md) <br>
- [Pass 4 Generate](references/pass-4-generate.md) <br>
- [Pass 5 Optimize](references/pass-5-optimize.md) <br>
- [Pass 6 Validate](references/pass-6-validate.md) <br>
- [Generic Platform Profile](profiles/generic.md) <br>
- [IR Schema](schemas/ir-schema.json) <br>
- [Trace Schema](schemas/trace-schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown report plus generated skill package files and JSON schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include a compilation report, folder tree, pass summary, evaluation results, cost summary, and generated skill files.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
