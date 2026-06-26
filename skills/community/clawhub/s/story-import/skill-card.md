## Description: <br>
Story Import reverse-parses an existing unfinished or completed novel into a standardized writing project structure for continuation with long-form or short-form story writing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers and writing agents use this skill to import an existing manuscript, analyze its structure, and rebuild it as a continuation-ready writing project. It supports both long novel and short story paths, including analysis assets, outline files, character state tracking, and source manuscript migration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retains the manuscript and derived analysis in multiple local project locations. <br>
Mitigation: Use it only when local retention is acceptable, choose the destination project deliberately, and remove retained copies when they are no longer needed. <br>
Risk: The import flow creates and migrates many project files, which may overwrite or conflict with existing writing-project assets. <br>
Mitigation: Run it in a dedicated project directory or review and back up existing project files before import. <br>
Risk: Generated analysis, outlines, and tracking files may be incomplete or inaccurate for the author's intended continuation plan. <br>
Mitigation: Review the generated structure, missing-item summary, and analysis assets before using downstream writing workflows. <br>


## Reference(s): <br>
- [Story Import ClawHub page](https://clawhub.ai/worldwonderer/skills/story-import) <br>
- [OpenClaw source link](https://github.com/worldwonderer/oh-story-claudecode) <br>
- [Length routing rules](references/length-routing.md) <br>
- [Long-form structure mapping](references/structure-mapping-long.md) <br>
- [Short-form structure mapping](references/structure-mapping-short.md) <br>
- [Format and structure rules](references/format-and-structure.md) <br>
- [State tracking protocol](references/state-tracking.md) <br>
- [Character state reverse rules](references/character-state-reverse.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown project files and concise conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local writing project assets, including manuscript copies, analysis files, outlines, character files, tracking files, and reference views.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
