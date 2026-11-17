## Description:

Generate dark-themed, tech-style PPTX presentations in 16:9 using python-pptx with customized slides, fonts, colors, and layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr1008611](https://clawhub.ai/user/mr1008611)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and presentation authors use this skill to turn a requested topic, outline, and content points into a dark, technology-styled PowerPoint deck. It provides reusable slide templates for cover, section, content, comparison, architecture, cards, table, and summary slides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local Python code to create a PowerPoint file.

Mitigation: Run it in a virtual environment with a reviewed and pinned python-pptx dependency.

Risk: Generated presentation files are returned through the platform.

Mitigation: Review the PPTX contents before sharing, especially when prompts include confidential or sensitive material.

Risk: The default visual style and fonts are Chinese-oriented.

Mitigation: Adjust the prompt, slide text, and font choices when a different language, brand, or accessibility requirement applies.

## Reference(s):


## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with Python code and a generated PPTX file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local .pptx presentation and returns the generated file to the user.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
