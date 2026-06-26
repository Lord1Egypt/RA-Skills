## Description: <br>
Verified Research guides agents through multi-source research, source-tiered verification, evidence capture, and structured Markdown report generation with a three-day local cache. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashanzzz](https://clawhub.ai/user/ashanzzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to perform deeper research tasks that require source planning, multi-source verification, evidence tracking, and a final structured report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics, evidence snippets, and conclusions may be cached locally and later written into MEMORY.md. <br>
Mitigation: Require explicit confirmation before researching sensitive topics, preserving summaries, or allowing MEMORY.md updates. <br>
Risk: Cached reports may be deleted by the three-day cleanup flow. <br>
Mitigation: Save reports that must be retained to the workspace before cleanup runs, and review cleanup actions for active research. <br>
Risk: The artifact describes updating its own skill instructions when methodology issues are found. <br>
Mitigation: Require explicit user review before any change to skill files or instructions. <br>


## Reference(s): <br>
- [Verified Research on ClawHub](https://clawhub.ai/ashanzzz/verified-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research reports with evidence-card Markdown files and JSON manifests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local three-day research cache and can archive summaries to MEMORY.md.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
