## Description: <br>
Analyzes long-form web novels through a staged workflow that backs up source text, produces golden-three-chapter analysis, chapter summaries, plot and pacing synthesis, character and setting files, a final deconstruction report, and a style profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External writers, editors, and story analysts use this skill to deconstruct legally held long-form fiction into reusable analysis of opening hooks, character architecture, plot rhythm, reader-emotion mechanics, settings, relationships, and prose style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves source novel text and derived analysis files in the workspace. <br>
Mitigation: Use it only with works you have the right to analyze and store, and review or delete `拆文库/{书名}/原文/` when the source text is sensitive. <br>
Risk: The workflow may update an existing `选题决策.md` planning file and resumed runs may overwrite the current resumed block's outputs. <br>
Mitigation: Review planning-file changes and existing progress state before resuming or rerunning analysis in a workspace with prior outputs. <br>


## Reference(s): <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Output Templates](artifact/references/output-templates.md) <br>
- [Material Decomposition](artifact/references/material-decomposition.md) <br>
- [Deconstruction Notes](artifact/references/deconstruction-notes.md) <br>
- [Pipeline Operations](artifact/references/pipeline-ops.md) <br>
- [Style Profile Protocol](artifact/references/style-profile-protocol.md) <br>
- [Style Profile Generator](artifact/references/style-profile-generator.md) <br>
- [OpenClaw Source Metadata](https://github.com/worldwonderer/oh-story-claudecode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown files and structured workspace directories] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates staged analysis artifacts under a novel-specific output directory, including source backup, progress state, chapter analyses, plot, character, setting, report, and style-profile files.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
