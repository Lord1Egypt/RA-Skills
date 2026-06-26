## Description: <br>
Run a lightweight YouTube transcript workflow: transcribe, attribution cleanup, translation, and packaging with minimal tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BlueBirdBack](https://clawhub.ai/user/BlueBirdBack) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and content teams use this skill to produce repeatable YouTube transcript handoffs with cleaned speaker attribution, optional translation, and a concise package of final files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Separate transcription or translation tools may introduce their own privacy, copyright, or security risks. <br>
Mitigation: Review the chosen transcription or translation tool before use and avoid processing private or copyrighted material unless permission is clear. <br>
Risk: Transcript cleanup can misattribute speakers or alter timestamp structure. <br>
Mitigation: Use conservative speaker reassignment, preserve timestamps and line counts, and validate final files against the source transcript. <br>


## Reference(s): <br>
- [Lite limits and defaults](references/limits.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with transcript text and handoff file structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewed transcript artifacts, optional translated transcripts, and a manifest while preserving timestamps and line structure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
