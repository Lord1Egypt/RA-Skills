## Description: <br>
Skill Release Plus helps developers package and publish an agent skill to ClawHub, skillhub.cn, GitHub Releases, or a trusted custom hook from one release command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to prepare a clean skill package, check publishing readiness, and release the same skill to one or more supported registries with a consistent version and changelog. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish skill contents to external services and create or push GitHub repositories and releases. <br>
Mitigation: Use --check and --dry-run before publishing, select only the intended target, and verify the resolved GitHub owner and repository before using github-release or --target all. <br>
Risk: Custom user-hook targets execute user-supplied scripts with local environment access. <br>
Mitigation: Run user-hook targets only from scripts that have been reviewed and are fully trusted. <br>
Risk: Publishing tokens are required for external services. <br>
Mitigation: Keep tokens narrowly scoped, provide only the tokens needed for the selected target, and avoid broad default target sets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/songhonglei/skill-release-plus) <br>
- [Documented source repository](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-release-plus) <br>
- [ClawHub CLI package](https://www.npmjs.com/package/clawhub) <br>
- [SkillHub.cn](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the release script emits JSON status reports and tar.gz package files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish to external services when invoked without --dry-run.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md Version field) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
