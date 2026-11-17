## Description:

Converts TRPG rules into a structured briefing_package for the TRPG AI GM engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ice26985850](https://clawhub.ai/user/ice26985850)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and TRPG content authors use this skill to convert rulebooks, scenarios, and character material into structured briefing_package files for a single-player AI GM experience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to modify active rulebooks, scenarios, or character sheets outside the intended briefing_package.

Mitigation: Use it in a version-controlled workspace and keep files outside briefing_package read-only unless you approve a precise file list and diff.

Risk: Converted briefing files can misrepresent source rules when the original material is ambiguous or incompatible with the package structure.

Mitigation: Review generated config, system prompt, rules, scenarios, data, and maps against the source rules before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown and YAML files in a briefing_package directory]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Traditional Chinese content; single-player TRPG scope; may pause with questions for ambiguous source rules.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
