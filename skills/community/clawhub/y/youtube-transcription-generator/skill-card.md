## Description: <br>
Generates YouTube video transcripts with optional timestamps by downloading media with yt-dlp and transcribing it with the VLM Run CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MehediAhamed](https://clawhub.ai/user/MehediAhamed) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to create readable transcripts from user-selected YouTube videos, with optional timestamped sections and saved transcript files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-selected media is processed by VLM Run for transcription. <br>
Mitigation: Avoid private, regulated, non-consensual, or copyrighted material unless the user has permission and accepts the provider's data-handling terms. <br>
Risk: The workflow downloads YouTube media locally before transcription. <br>
Mitigation: Use only valid public URLs and confirm the user has the rights and policy clearance to download and process the content. <br>
Risk: The skill requires a VLMRUN_API_KEY stored in .env or .env.local. <br>
Mitigation: Protect the API key as a secret and avoid exposing it in transcripts, logs, shared output directories, or source control. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text or Markdown transcript content with optional timestamps, plus command and setup guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save transcript files and downloaded media artifacts in a user-selected output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
