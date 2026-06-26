## Description: <br>
Proofread SRT subtitles by using srts/source.md as terminology reference while preserving subtitle indices and timestamps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KapiAI](https://clawhub.ai/user/KapiAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Subtitle editors, localization reviewers, and agents use this skill to proofread a single srts/*.srt file against srts/source.md terminology while keeping subtitle numbering, timestamps, and structure intact. It supports larger subtitle files by splitting them into sections, editing each section, and merging them back under git-tracked review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may stage unrelated or sensitive files if the srts/ folder contains content beyond the subtitle task. <br>
Mitigation: Use a dedicated srts/ folder, remove unrelated or sensitive files before git add . runs, and review the final git diff before accepting changes. <br>
Risk: Subtitle files can become invalid if edits change sequence numbers, timestamp lines, or structural blank lines. <br>
Mitigation: Keep edits limited to subtitle text and verify the final git diff shows unchanged indices, timestamps, and subtitle block boundaries. <br>
Risk: Large-file handling splits and then overwrites the main SRT file during merge-back. <br>
Mitigation: Create or keep the git baseline before splitting, then review the merged output and final diff before accepting the rewritten main SRT file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KapiAI/srt-proofreader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown summary with git diff review guidance and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Edits local SRT subtitle text while preserving sequence numbers, timestamp lines, and blank-line boundaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
