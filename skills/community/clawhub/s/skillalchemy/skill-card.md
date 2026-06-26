## Description: <br>
Skill Alchemy Main orchestrates Lens and LEAP to turn a user's idea, source person, method, or existing skills into an installable SKILL.md. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentsope](https://clawhub.ai/user/agentsope) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to distill public source material into persona or methodology skills, or to fuse existing skills into a new installable skill. It is intended as the interactive entry point that manages user checkpoints while Lens and LEAP perform analysis and compilation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated skills may incorporate untrusted public skill text fetched from public skill indexes or source repositories. <br>
Mitigation: Review and scan each generated SKILL.md before installing it, especially before using it on private or sensitive tasks. <br>
Risk: The release metadata advertises financial, purchasing, paid-service, OAuth, and credential-related capability tags that are not clearly scoped by the artifact. <br>
Mitigation: Do not grant financial authority, purchase permission, OAuth tokens, paid-service access, or secrets unless a local review confirms that the generated skill actually requires them. <br>
Risk: All-default operation can reduce checkpoints before generated instructions are installed. <br>
Mitigation: Use step-by-step or deep mode for sensitive work and inspect the research plan, generated skill, and validation notes before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentsope/skillalchemy) <br>
- [README_EN.md](README_EN.md) <br>
- [Technical Documentation](技术文档.md) <br>
- [Skill Grammar Reference](skills/LEAP/references/skill-grammar.md) <br>
- [SkillsBench](https://github.com/benchflow-ai/skillsbench) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown files, JSON planning artifacts, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create an output/<target>-skill/ directory containing a generated SKILL.md, intermediate evidence, research plans, and validation notes.] <br>

## Skill Version(s): <br>
0.1.3 (source: ClawHub release metadata; artifact frontmatter, package.json, and CHANGELOG report v1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
