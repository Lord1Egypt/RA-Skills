## Description:

Generates a deployable HTML introduction page for an AgentSkill from USAGE.md or SKILL.md, with themed layouts, feature cards, quick start content, navigation, and an optional trusted deploy hook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to turn an AgentSkill's documentation into a polished local or deployable HTML introduction page. It is useful for publishing skill documentation with themed presentation, quick start sections, command examples, and navigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated pages can include unsafe code from malicious or untrusted skill documentation.

Mitigation: Generate pages only from trusted skill sources, review the resulting HTML before publishing, and treat generated HTML as unsafe until escaping and URL validation are fixed.

Risk: The optional deploy hook can publish generated output through a local command.

Mitigation: Use --no-deploy by default and configure SKILL_INTRO_DEPLOY_CMD only to a trusted local script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/songhonglei/skills/skill-introduction)
- [Declared repository link](https://github.com/Songhonglei/skill-introduction)
- [Mistune documentation](https://mistune.lepture.com/)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Configuration, Guidance]

**Output Format:** [HTML file plus Markdown and shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate local HTML output and optionally invoke a trusted deploy hook configured by environment variable.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
