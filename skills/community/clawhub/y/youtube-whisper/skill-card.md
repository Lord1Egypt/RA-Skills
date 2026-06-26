## Description: <br>
Downloads YouTube subtitles or audio and uses local Whisper to produce transcript text, with Traditional Chinese as the default output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dolphins1123](https://clawhub.ai/user/dolphins1123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn YouTube videos into transcripts for notes, subtitle preparation, or summaries. The agent can summarize the transcript after transcription when the user asks for a summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads or extracts YouTube subtitles and audio, which may include copyrighted, private, or sensitive content. <br>
Mitigation: Use it only with content you have permission to process, and review generated transcripts before sharing or reusing them. <br>
Risk: Local Whisper transcription can consume significant CPU, memory, and disk resources, especially when --force skips resource checks. <br>
Mitigation: Keep resource checks enabled unless you accept the extra load, choose an appropriate Whisper model, and reserve enough local storage before running. <br>
Risk: Transcript files are written to the selected output path and could overwrite or expose local files if the path is chosen carelessly. <br>
Mitigation: Use a dedicated output filename or directory and inspect the resulting file path before relying on or sharing the transcript. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text transcript with a processing summary and optional transcript file path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write transcript text files to a user-selected output path; long transcript output is surfaced as a file path.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
