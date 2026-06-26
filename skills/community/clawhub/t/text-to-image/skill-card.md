## Description: <br>
Renders styled plain text into SVG, PNG, JPG, or JPEG image files with size, font, color, highlight, wrapping, and optional data URI controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erickong](https://clawhub.ai/user/erickong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn text, captions, slogans, multilingual content, and highlighted text spans into local image files for upload or downstream use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Custom output paths can write generated images outside the default temporary folder and may target existing or sensitive files. <br>
Mitigation: Use the default temporary output for routine use and provide a custom output path only when that destination is intentional. <br>
Risk: Untrusted custom font files can affect local rendering behavior. <br>
Mitigation: Use custom font paths only with font files from trusted sources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/erickong/text-to-image) <br>
- [Publisher Profile](https://clawhub.ai/user/erickong) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [Local image file plus JSON metadata, with optional data URI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports SVG, PNG, JPG, and JPEG output with configurable dimensions, colors, highlights, wrapping, alignment, and font sizing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
