## Description: <br>
Capture frames or clips from RTSP/ONVIF cameras. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosrider](https://clawhub.ai/user/cosrider) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide command-line discovery, setup, diagnostics, and capture workflows for configured RTSP/ONVIF cameras. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Camera credentials or network details may be exposed in shared shell history, transcripts, or configuration files. <br>
Mitigation: Use limited camera accounts, avoid pasting real passwords into shared contexts, and restrict permissions on the camera configuration file. <br>
Risk: Snapshots, clips, and motion events can contain sensitive video data. <br>
Mitigation: Store captures deliberately, limit access to output files, and run short test captures before longer recordings. <br>
Risk: Motion-watch actions can execute unintended commands if configured carelessly. <br>
Mitigation: Configure only motion-watch actions that have been reviewed and are intended to run in the target environment. <br>
Risk: The skill depends on an external Homebrew tap and media tooling. <br>
Mitigation: Install only when the camsnap Homebrew tap and dependencies are trusted, and verify ffmpeg is available on PATH. <br>


## Reference(s): <br>
- [Camsnap homepage](https://camsnap.ai) <br>
- [ClawHub skill page](https://clawhub.ai/cosrider/xxx) <br>
- [Publisher profile](https://clawhub.ai/user/cosrider) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may reference local camera configuration, ffmpeg availability, and capture file paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
