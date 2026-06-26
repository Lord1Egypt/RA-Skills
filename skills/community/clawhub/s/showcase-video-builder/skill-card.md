## Description: <br>
Build polished showcase and demo videos from screenshots, avatars, and text overlays using ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, hackathon teams, OSS maintainers, and product teams use this skill to turn static screenshots, avatars, and text into showcase videos, demo reels, product walkthroughs, or social clips without a full video editor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the helper on the wrong image folder or output path can process unintended local files or overwrite an expected video artifact. <br>
Mitigation: Run it only on image folders you choose and review the output path before execution. <br>
Risk: The skill metadata includes sensitive-credential capability tags even though the documented workflow does not require credentials. <br>
Mitigation: Do not provide OAuth tokens or other sensitive credentials when using this local ffmpeg workflow. <br>
Risk: The workflow depends on a local ffmpeg installation, and some ffmpeg builds may lack text-rendering support. <br>
Mitigation: Confirm ffmpeg is installed and test the command on disposable sample images before using it for final media. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nissan/showcase-video-builder) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with ffmpeg command examples and shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local video-building instructions and commands; generated media files are created by ffmpeg when the user runs the commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
