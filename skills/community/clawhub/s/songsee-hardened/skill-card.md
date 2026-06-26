## Description: <br>
Generate spectrograms and feature-panel visualizations from audio with the songsee CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to ask an agent for local songsee commands that turn audio files or stdin streams into spectrograms and multi-panel audio feature visualizations while following guardrails for sensitive audio, resource use, and network transmission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated visualizations or source audio could be sent outside the local machine if shell commands pipe songsee output to network tools. <br>
Mitigation: Keep outputs local by saving files with songsee options such as -o, and do not pipe audio or generated images to network-transmitting commands. <br>
Risk: Manual ffmpeg commands can expand the workflow beyond audio visualization and introduce network, streaming, or arbitrary filter behavior. <br>
Mitigation: Pass supported audio files directly to songsee and let songsee handle non-native format conversion internally when ffmpeg is available. <br>
Risk: Very large dimensions, many visualization panels, or long audio can consume substantial disk or memory resources. <br>
Mitigation: Confirm intent before using dimensions above 5000px, all visualization panels at once, or audio longer than 60 minutes. <br>
Risk: Audio filenames suggesting therapy, medical, legal, meeting, or private content may involve sensitive recordings. <br>
Mitigation: Ask the user to confirm before processing sensitive-looking audio and keep generated visualizations local. <br>


## Reference(s): <br>
- [Songsee project homepage](https://github.com/steipete/songsee) <br>
- [Faberlens songsee safety evaluation](https://faberlens.ai/explore/songsee) <br>
- [ClawHub release page](https://clawhub.ai/snazar-faberlens/songsee-hardened) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target local songsee CLI workflows and may require user confirmation for sensitive audio or high-resource processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
