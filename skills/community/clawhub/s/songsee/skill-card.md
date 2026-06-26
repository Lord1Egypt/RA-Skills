## Description: <br>
Generate spectrograms and feature-panel visualizations from audio with the songsee CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, audio engineers, and analysts use this skill to generate spectrograms, time slices, and multi-panel audio feature visualizations from selected audio files with the songsee CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on an external Homebrew tap and the songsee CLI. <br>
Mitigation: Install only after deciding that the tap and CLI are trusted for the target environment. <br>
Risk: The CLI processes user-selected audio inputs and writes visualization outputs. <br>
Mitigation: Run commands only on audio files and output locations chosen for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/steipete/songsee) <br>
- [Declared project homepage](https://github.com/steipete/songsee) <br>
- [Homebrew formula](https://github.com/steipete/homebrew-tap) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples for songsee CLI usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the songsee CLI from Homebrew formula steipete/tap/songsee; formats beyond native WAV/MP3 decoding may require ffmpeg.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
