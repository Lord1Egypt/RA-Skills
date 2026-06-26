## Description: <br>
A guide for downloading Bilibili videos, cropping borders, trimming clips, and compressing them for Xiaomi touchscreen alarm clock playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mimose101](https://clawhub.ai/user/mimose101) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media-focused agent users can use this skill to produce compact alarm-clock-ready videos from Bilibili sources by following download, crop, trim, and compression steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local media-processing commands and package installation may affect the user's environment. <br>
Mitigation: Install dependencies intentionally, preferably in a Python virtual environment, and review commands before execution. <br>
Risk: Downloaded or processed videos can be overwritten or produce an unsuitable final file. <br>
Mitigation: Use unique BV-number-based filenames, keep originals, and confirm the cropped, trimmed, and compressed output before deleting intermediate files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mimose101/xiaomi-touchscreen-alarm-clock-video-production) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command plans and processing settings; media files are changed only if the agent or user executes the commands.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
