## Description: <br>
Publishes Agent skills to multiple platforms including ClawHub, GitHub Releases, and SkillHub CN, with validation, packaging, version management, and one-command multi-platform publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlx](https://clawhub.ai/user/zlx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to validate, package, version, and publish local Agent skills to supported distribution platforms. It is most useful for release workflows that need repeated publication to ClawHub, GitHub Releases, or SkillHub CN. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing may package and upload the entire target skill directory to the selected platforms. <br>
Mitigation: Review the target directory contents before publishing and use only platforms where that upload is intended. <br>
Risk: Platform adapters can execute publishing logic with local credentials or authenticated CLIs. <br>
Mitigation: Review added or modified adapters before use and avoid running unknown adapters. <br>
Risk: Sensitive-keyword scanning is not a complete secret-leak prevention control. <br>
Mitigation: Perform separate secret scanning and manual review before release. <br>


## Reference(s): <br>
- [Skill Publisher Release Page](https://clawhub.ai/zlx/skill-publisher-zlx) <br>
- [Adding Platforms](references/adding-platforms.md) <br>
- [Platform Interface](references/platform-interface.md) <br>
- [SkillHub CN](https://skillhub.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local platform adapters and publishing CLIs that require authentication before release.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
