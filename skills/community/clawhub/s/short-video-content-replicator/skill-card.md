## Description: <br>
Automates a six-step short-video workflow that downloads Douyin or Bilibili videos or resumes from local media, extracts vocals, transcribes speech, corrects text, and restores punctuation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangminrui2022](https://clawhub.ai/user/wangminrui2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to process short-form video links or local media into clean vocal audio and punctuated text for content reuse, transcription, batch processing, or TTS preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow creates local media and text files and depends on companion media-processing skills. <br>
Mitigation: Use a specific output directory, confirm the companion skills are trusted and installed, and review generated files before relying on them. <br>
Risk: Downloading or processing third-party videos can raise copyright or privacy concerns. <br>
Mitigation: Process only content you are allowed to use and consider copyright and privacy implications before downloading or transforming videos. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangminrui2022/short-video-content-replicator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and local media/text file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces videos, MP3 audio, vocal WAV files, transcripts, corrected text, and punctuated final text under an output directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
