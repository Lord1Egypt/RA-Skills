## Description: <br>
Download a TikTok, Instagram Reel, X video, or short-form video URL locally, extract/transcribe the audio, analyse the teaching or workflow inside it, and turn it into a concise OpenClaw skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olliewazza](https://clawhub.ai/user/olliewazza) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn a user-provided short-form social video into a reusable OpenClaw skill by downloading the media, transcribing audio when available, and extracting the repeatable workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script stores downloaded video, extracted audio, transcripts, and result metadata locally. <br>
Mitigation: Use a controlled output directory, remove local media artifacts when no longer needed, and avoid processing videos that contain sensitive content unless local storage is acceptable. <br>
Risk: If OPENAI_API_KEY is set, audio may be sent to OpenAI for transcription. <br>
Mitigation: Unset OPENAI_API_KEY for local-only behavior, or confirm that external transcription is acceptable for the provided media before running the script. <br>
Risk: The generated skill may preserve incorrect or incomplete process details from the source video. <br>
Mitigation: Review and scan the generated skill before using or publishing it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/olliewazza/reel-to-skill) <br>
- [OpenAI audio transcription endpoint used by the helper script](https://api.openai.com/v1/audio/transcriptions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown skill instructions with optional generated files and JSON helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local video, audio, transcript, and result JSON files under the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
