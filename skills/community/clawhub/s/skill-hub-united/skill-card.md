## Description:

Installs skills from ClawHub, SkillHub, skills.sh, Anthropic's skills repository, or a configured self-hosted hub based on the user's request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use the installer to add a named skill from the hub they specify, resolve name conflicts, and handle source-specific license restrictions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports destination-safety concerns.

Mitigation: Validate the installation destination and avoid installing until destination handling has been addressed.

Risk: Automatic use of unpinned packages can install changed content.

Mitigation: Pin package versions or review the exact release before allowing automated installation.

Risk: Security analysis is incomplete because three local references could not be resolved.

Mitigation: Review unresolved references and rescan the complete package before relying on the security assessment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/songhonglei/skills/skill-hub-united)
- [ClawHub](https://clawhub.ai)
- [SkillHub](https://skillhub.cn)
- [skills.sh](https://skills.sh)
- [Anthropic Skills repository (install source)](https://github.com/anthropics/skills)

## Skill Output:

**Output Type(s):** [Files, Text, JSON]

**Output Format:** [Installed skill files with text status messages; JSON for structured conflict or license outcomes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available files and status details depend on the selected source and installer outcome.]

## Skill Version(s):

1.0.7 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
