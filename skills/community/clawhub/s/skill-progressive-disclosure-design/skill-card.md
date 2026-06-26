## Description: <br>
Decide how to split skill content between SKILL.md and reference files for context efficiency and reliable triggering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to decide whether, when, and how to split agent skill content between SKILL.md, references, and scripts while preserving reliable triggering and context efficiency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose edits to skill structure or guidance that are incorrect for a specific repository. <br>
Mitigation: Review proposed file edits before applying them, and scan the skill before deployment. <br>
Risk: Architecture evaluation transcripts may contain private code, prompts, or project details. <br>
Mitigation: Avoid storing or sharing generated eval transcripts when they include private information. <br>


## Reference(s): <br>
- [Source repository](https://github.com/samber/cc-skills) <br>
- [ClawHub release page](https://clawhub.ai/samber/skill-progressive-disclosure-design) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional code, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend concrete SKILL.md pointer text, reference-file structure, eval instrumentation, and review of proposed file edits before applying them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
