## Description: <br>
Search skills.sh registry from CLI. Find and discover agent skills from the skills.sh ecosystem. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheSethRose](https://clawhub.ai/user/TheSethRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to search the skills.sh registry, list popular skills, and inspect suggested install commands from a terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Displayed install commands may point to third-party skills that have their own source, scope, and security properties. <br>
Mitigation: Review the target skill, its source, and its requested scope before adding it to an agent environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/TheSethRose/skills-search) <br>
- [skills.sh](https://skills.sh) <br>
- [skills.sh skills API](https://skills.sh/api/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Terminal text with optional install command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and network access to the skills.sh API.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
