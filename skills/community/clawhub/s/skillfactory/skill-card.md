## Description: <br>
Skill Factory turns skill ideas or upgrade requests into structured OpenClaw skill packages by guiding capture, source collection, distillation, publishing, versioning, and maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhelunsun](https://clawhub.ai/user/zhelunsun) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and skill authors use Skill Factory to create or upgrade OpenClaw skills from ideas, notes, or source URLs, then package them for GitHub or ClawHub distribution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through broad file creation, synchronization, and publishing workflows. <br>
Mitigation: Require explicit confirmation before file writes, force sync, git push/tag, ClawHub publish, or recurring automation. <br>
Risk: Loose activation or unclear user intent could lead to unwanted skill creation or maintenance actions. <br>
Mitigation: Use explicit commands and review the resolved target path and generated plan before allowing the workflow to proceed. <br>
Risk: Source collection may involve web access and third-party material. <br>
Mitigation: Require separate confirmation before web access and review collected sources before distillation or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhelunsun/skillfactory) <br>
- [Repository](https://github.com/zhelunSun/skill-factory) <br>
- [README](README.md) <br>
- [Skill SOP](SKILL.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline command examples and file-structure templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow plans and proposed files that should be reviewed before execution or publication.] <br>

## Skill Version(s): <br>
2.4.0 (source: frontmatter, changelog, server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
