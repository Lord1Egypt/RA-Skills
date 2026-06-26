## Description: <br>
Video Frames helps agents guide installation, troubleshooting, and use of a PyAV-based command-line tool for extracting, sampling, inspecting, and compressing video frames and image outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indulgeback](https://clawhub.ai/user/indulgeback) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media-processing users use this skill to install and operate a local frame-extraction CLI for single-frame capture, batch sampling, video inspection, H.264 video compression, and WebP image conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The automatic install path runs a mutable remote shell script and may add files under the user's home directory or modify shell PATH configuration. <br>
Mitigation: Prefer manual installation or download and inspect the installer before running it; verify install, cleanup, and PATH commands before copying them. <br>
Risk: Successful use depends on local Python, virtual environment, PyAV, Pillow, tqdm, and FFmpeg-related setup. <br>
Mitigation: Run the bundled diagnostic workflow before relying on the CLI and use the manual dependency repair steps when checks fail. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/indulgeback/video-frames-skill) <br>
- [Publisher profile](https://clawhub.ai/user/indulgeback) <br>
- [Project homepage listed in artifact metadata](https://github.com/indulgeback/video-frame-extractor) <br>
- [Installer URL listed in artifact metadata](https://raw.githubusercontent.com/indulgeback/video-frame-extractor/main/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, PATH setup, dependency checks, diagnostic commands, and CLI usage examples for local media processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
