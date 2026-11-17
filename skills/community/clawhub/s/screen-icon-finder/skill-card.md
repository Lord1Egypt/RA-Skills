## Description:

Screen Icon Finder helps an agent locate a target icon in a screenshot or full-screen capture using OpenCV template matching, mark matches with scores, and optionally click a matched center point.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lieyingthh](https://clawhub.ai/user/lieyingthh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and desktop automation agents use this skill to find a small target image within a larger screenshot, return match coordinates and confidence, annotate results, and optionally click a found icon.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture the full screen, which may include sensitive information.

Mitigation: Use an explicit non-sensitive screenshot when possible and avoid running it on screens containing confidential data.

Risk: The skill can leave captured and annotated screenshots on disk.

Mitigation: Delete _temp_screen.png and _result.png after use, especially when screenshots may contain private content.

Risk: The skill can guide clicks on the active desktop based on template-matching results.

Mitigation: Review the annotated result and coordinates before allowing any click action.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, code, shell commands, files, guidance]

**Output Format:** [Markdown or plain text with Python and shell command snippets, coordinate results, and generated annotated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create _temp_screen.png for full-screen capture and _result.png for annotated matches.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
