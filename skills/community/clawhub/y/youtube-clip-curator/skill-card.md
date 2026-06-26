## Description: <br>
Analyze long YouTube videos to extract ranked clip candidates with timestamps, titles, hooks, emotion tags, and optional edit project files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noahcraft-open](https://clawhub.ai/user/noahcraft-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, editors, and social video teams use this skill to turn long-form YouTube videos, streams, podcasts, or transcripts into a ranked set of short clip candidates ready for review and editing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video files, transcripts, and style references may contain sensitive or private content. <br>
Mitigation: Only provide media, transcripts, and reference channels that are appropriate for agent analysis. <br>
Risk: Generated editing scripts or XML can alter production timelines when imported into editing tools. <br>
Mitigation: Review generated FCPXML, DaVinci Resolve scripts, and subtitle files before importing them into production projects. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON, FCPXML, DaVinci Resolve script, thumbnail brief JSON, or SRT subtitle outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include ranked clip candidates with start and end timestamps, hook descriptions, title suggestions, emotion tags, scores, and reasons.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
