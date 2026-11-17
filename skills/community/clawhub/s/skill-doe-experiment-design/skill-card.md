## Description:

Generates full-factorial and fractional-factorial DOE plans with configurable factors, levels, resolution settings, CSV export, and structured JSON summaries for experiment planning and data analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quality engineers, and experiment owners use this skill to generate DOE run matrices for screening and analysis workflows. It is most useful when a user needs a full-factorial design, a two-level fractional-factorial design, or a CSV plan that can be reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generator can overwrite writable files when given an existing or unsafe output path.

Mitigation: Run it in a dedicated output directory, avoid absolute or parent-traversal paths, and check whether the target CSV already exists before execution.

Risk: Large factor or level counts can produce very large designs and unbounded output.

Mitigation: Use small DOE dimensions unless resource limits have been reviewed for the workspace.

Risk: The skill mentions Taguchi and orthogonal designs, but the security guidance warns not to rely on it for Taguchi or true orthogonal-array design without validation.

Mitigation: Independently validate generated designs before using them for Taguchi methods, orthogonal arrays, or consequential experiment decisions.

## Reference(s):

- [DOE experiment design guide](references/doe_guide.md)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-doe-experiment-design)
- [Publisher profile](https://clawhub.ai/user/duding-engicool)
- [Server-resolved GitHub source](https://github.com/duding-engicool/skill-doe-experiment-design)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell command examples; the bundled script emits JSON summaries and writes CSV design files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CSV output paths and DOE dimensions are user supplied; pandas is required to run the generator script.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
