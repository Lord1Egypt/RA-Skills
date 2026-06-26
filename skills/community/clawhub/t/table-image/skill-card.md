## Description: <br>
Generate images from tables for better readability in messaging apps like Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joargp](https://clawhub.ai/user/joargp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Table Image to convert Markdown tables into PNG images for messaging platforms that do not render Markdown tables well. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install an external Go CLI from GitHub, including an @latest install path. <br>
Mitigation: Review or pin the tablesnap version before installation in stricter environments. <br>
Risk: Full emoji support may download additional emoji assets. <br>
Mitigation: Enable the emoji asset download only in environments where external downloads are allowed and reviewed. <br>
Risk: Unsupported emoji render as placeholder boxes until full emoji support is installed. <br>
Mitigation: Install the full emoji set when emoji fidelity matters, or limit table content to the bundled supported emoji. <br>


## Reference(s): <br>
- [Table Image ClawHub release page](https://clawhub.ai/joargp/table-image) <br>
- [tablesnap repository](https://github.com/joargp/tablesnap) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and MEDIA file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PNG table images via the tablesnap CLI, commonly written to /tmp/table.png; full emoji support may require a one-time asset download.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
