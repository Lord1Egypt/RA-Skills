## Description:

Generates a Chinese-language 15-slide interior design presentation framework from a SketchUp file path, with placeholder pages for manually inserted SketchUp screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[137984917-cyber](https://clawhub.ai/user/137984917-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Interior design practitioners use this skill to create a standardized client presentation deck for SketchUp-based projects. It produces the PPT framework and leaves visual effect pages ready for screenshots exported separately from SketchUp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documentation overstates SketchUp automation and may imply model analysis or screenshot capture that the artifact does not provide.

Mitigation: Use it as a PPT framework generator and manually export or insert SketchUp screenshots into the reserved slides.

Risk: The script may overwrite the output PPTX path supplied by the user.

Mitigation: Choose a new output path or back up any existing presentation before running the script.

Risk: The script appears to return an undefined variable after saving, so it may report an error even when the PPTX file was created.

Mitigation: Check whether the output PPTX exists after execution and review the generated file before treating the run as failed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/137984917-cyber/skills/sketchup-ppt-generator)
- [Publisher profile](https://clawhub.ai/user/137984917-cyber)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash usage examples and a Python script that writes a PPTX file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local SketchUp file path and an output PPTX path; the generated deck uses a fixed 15-page framework.]

## Skill Version(s):

1.0.0 (source: release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
