## Description:

Generates deterministic, self-contained HTML/SVG decision flowcharts from SKILL.md files or skill definitions by having an agent extract nodes.json and a Python script render the layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codermoray](https://clawhub.ai/user/codermoray)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to turn natural-language skill definitions into structured flowchart node data and render that data as portable HTML/SVG diagrams for review, documentation, and workflow visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML from untrusted skill definitions may carry content-handling risk.

Mitigation: Use trusted or reviewed nodes.json inputs and avoid opening generated HTML from untrusted sources until loop labels are escaped, legend colors are validated, and a restrictive Content Security Policy is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codermoray/skills/skill-flowchart)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with JSON node data and shell commands that produce self-contained HTML/SVG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The rendered flowchart is deterministic for the same nodes.json input and supports light, dark, and transparent themes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
