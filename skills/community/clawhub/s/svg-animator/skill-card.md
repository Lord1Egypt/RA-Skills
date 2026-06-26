## Description: <br>
SVG Animator helps agents generate SVG-frame animations and assemble them into MP4 or GIF outputs for animals, scenes, abstract motion, and short stories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juliantsaiii](https://clawhub.ai/user/juliantsaiii) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creative automation users can use this skill to produce simple animated videos or GIFs from text-described SVG frame sequences, including single actions and multi-scene stories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script runs local media-conversion shell commands and writes files on the user's machine. <br>
Mitigation: Use trusted ffmpeg and rsvg-convert binaries, run without elevated privileges, and review generated commands before execution. <br>
Risk: Untrusted or complex output paths and very large frame counts can create avoidable local execution or resource risks. <br>
Mitigation: Keep output paths simple and trusted, limit frame counts, and avoid publishing generated files through nginx unless public access is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juliantsaiii/svg-animator) <br>
- [Publisher profile](https://clawhub.ai/user/juliantsaiii) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples, producing SVG frames and MP4 or GIF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media depends on local ffmpeg and rsvg-convert availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
