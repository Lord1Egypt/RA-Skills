## Description: <br>
macOS CLI tool to record microphone audio, screen video or screenshots, and camera video or photos from the terminal with device listing and output control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atacan](https://clawhub.ai/user/atacan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and terminal-based agents use this skill on macOS to capture short audio, screen, screenshot, webcam video, or photo artifacts while selecting devices, displays, windows, durations, and output paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive microphone, screen, and camera capture. <br>
Mitigation: Confirm each recording request with the user, including what will be captured, the duration, and the output path. <br>
Risk: The skill relies on a third-party Homebrew tap for installation. <br>
Mitigation: Install only when the publisher and tap are trusted for the target environment. <br>
Risk: Long or open-ended recording can capture more sensitive data than intended. <br>
Mitigation: Prefer short explicit durations, window or region capture when possible, and revoke microphone, camera, or screen permissions when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/atacan/record) <br>
- [Publisher profile](https://clawhub.ai/user/atacan) <br>
- [Audio command reference](references/audio.md) <br>
- [Screen command reference](references/screen.md) <br>
- [Camera command reference](references/camera.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command option tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The described CLI can emit file paths or JSON to stdout; recordings and captures are written to user-selected or temporary file paths.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
