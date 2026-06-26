## Description: <br>
Guide for running the Video Generator CLI commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itspremkumar](https://clawhub.ai/user/itspremkumar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to choose the appropriate Video Generator CLI command for fresh generation, recovery, segment assembly, debugging, and JSON script configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fresh-start commands remove prior generated cache, video, and audio outputs. <br>
Mitigation: Use resume or segment commands when preserving existing work matters, and back up generated outputs before running npm run generate or npm run build. <br>
Risk: External stock-footage or voiceover services may receive script content during generation workflows. <br>
Mitigation: Avoid confidential scripts unless those services are approved for the content being processed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/itspremkumar/video-gen-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [References CLI prerequisites: node, npm, ffmpeg, python, and PEXELS_API_KEY.] <br>

## Skill Version(s): <br>
5.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
