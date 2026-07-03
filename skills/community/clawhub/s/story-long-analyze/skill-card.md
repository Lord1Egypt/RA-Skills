## Description: <br>
Story Long Analyze helps agents analyze long-form web novels through a staged pipeline covering opening chapters, character architecture, pacing, payoff design, chapter summaries, setting relationships, reports, and style profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and developers use this skill to break down legally available long-form fiction into reusable narrative analysis, including chapter summaries, character and setting notes, pacing maps, reader-payoff patterns, and style profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill preserves full copies of supplied manuscripts in the project workspace. <br>
Mitigation: Use a disposable workspace for private, unpublished, licensed, or sensitive text, and remove 拆文库/{书名}/原文/ after the run if retention is not desired. <br>
Risk: The skill may update the root-level planning file 选题决策.md when that file exists. <br>
Mitigation: Review any 选题决策.md changes before keeping them. <br>


## Reference(s): <br>
- [OpenClaw source](https://github.com/worldwonderer/oh-story-claudecode) <br>
- [Deconstruction Notes](references/deconstruction-notes.md) <br>
- [Material Decomposition](references/material-decomposition.md) <br>
- [Output Templates](references/output-templates.md) <br>
- [Pipeline Operations](references/pipeline-ops.md) <br>
- [Style Profile Generator](references/style-profile-generator.md) <br>
- [Style Profile Protocol](references/style-profile-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown files and structured analysis notes written into a project workspace] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates staged outputs under 拆文库/{书名}/ and may update 选题决策.md when that file exists.] <br>

## Skill Version(s): <br>
1.1.9 (source: ClawHub release evidence; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
