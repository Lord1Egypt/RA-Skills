## Description: <br>
YouTube channel monitor and video transcription skill that uses AssemblyAI cloud transcription to return transcript text and an AI summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azazlf09](https://clawhub.ai/user/azazlf09) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content-monitoring users use this skill to add YouTube channels, check for new videos, transcribe videos through AssemblyAI, and save transcript summaries for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video audio URLs and resulting transcript data are sent to AssemblyAI for cloud processing. <br>
Mitigation: Use only approved content, avoid confidential or regulated material unless authorized, and review AssemblyAI handling requirements before use. <br>
Risk: Transcripts and summaries may contain sensitive content and are saved locally. <br>
Mitigation: Delete saved summaries when they are no longer needed and prefer the ASSEMBLYAI_API_KEY environment variable over storing credentials in data/config.json. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/azazlf09/yt-assemblyai-monitor) <br>
- [AssemblyAI signup](https://www.assemblyai.com/app/signup) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Console output and JSON files containing transcript text, summaries, confidence scores, and utterance segments.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AssemblyAI API key and writes summaries under data/summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
