## Description:

Converts complex Venn diagrams with more than four sets into clearer Upset Plot visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to transform multi-set overlap data into Upset Plot PNG visualizations and review intersection statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned plotting dependencies can change behavior across environments.

Mitigation: Install in an isolated environment and pin matplotlib and numpy before production use.

Risk: The plotting workflow writes files to the local filesystem.

Mitigation: Provide only the intended output path and review generated files before sharing them.

Risk: Unexpected or incomplete set data can produce misleading intersection visualizations.

Mitigation: Validate input set names, element lists, subset thresholds, and maximum intersections before generating the plot.

## Reference(s):


## Skill Output:

**Output Type(s):** [Files, Analysis, Guidance, Shell commands]

**Output Format:** [Markdown guidance with optional Python or shell snippets and local PNG plot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes visualization output to a user-provided local path; prints intersection statistics when run as an example script.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
