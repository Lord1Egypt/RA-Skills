## Description:

Generates minimalist geometric WeChat Mini Program TabBar icons with Python PIL and updates app.json with unselected and selected icon paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flowstart](https://clawhub.ai/user/flowstart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building WeChat Mini Programs use this skill to generate consistent 81x81 PNG TabBar icons, match icons to tab labels or page paths, and update the project's app.json tabBar configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill edits project files, including app.json and generated assets under images/.

Mitigation: Review the target project path and app.json changes before accepting the edits.

Risk: Pillow installation or version drift can affect reproducibility across environments.

Mitigation: Install Pillow in a virtual environment with a pinned version when reproducible builds are required.

Risk: Automatic tab label matching can choose an unintended icon for ambiguous tab names.

Mitigation: Confirm unmatched or ambiguous tab mappings and inspect the generated TabBar icons before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flowstart/skills/wx-tabbar-icons)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python and shell command examples, plus generated PNG files and app.json configuration updates when executed by an agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates paired unselected and selected 81x81 PNG icons for each tab and writes iconPath and selectedIconPath entries into app.json.]

## Skill Version(s):

1.0.0 (source: package.json and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
