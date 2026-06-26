## Description: <br>
Weekly retrospective that analyzes memory logs to identify accomplishments, recurring patterns, friction points, and forward-looking recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn weekly memory logs into a strategic retrospective with accomplishments, recurring patterns, friction points, unfinished work, recommendations, and a week score. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local memory logs and workspace context files that may contain sensitive personal or work details. <br>
Mitigation: Review configured memory, SOUL.md, AGENTS.md, and related input paths before running the skill. <br>
Risk: Generated retrospectives and optional history summaries may retain sensitive summaries on disk. <br>
Mitigation: Choose output and history locations deliberately, restrict access to those files, and review generated reports before sharing. <br>


## Reference(s): <br>
- [Retrospective Format Reference](references/retro-format.md) <br>
- [Weekly Retro on ClawHub](https://clawhub.ai/newageinvestments25-byte/weekly-retro) <br>
- [Publisher Profile](https://clawhub.ai/user/newageinvestments25-byte) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown retrospective with YAML frontmatter, plus JSON analysis and optional history records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Obsidian-compatible report output; Python standard library only.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
