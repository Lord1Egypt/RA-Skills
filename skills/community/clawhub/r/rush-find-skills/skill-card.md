## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krislavten](https://clawhub.ai/user/krislavten) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to search a reskill-compatible registry for relevant agent skills, review matching results, and install selected skills into supported agent environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package-manager workflows can install third-party skills from a registry into an agent environment. <br>
Mitigation: Review the registry URL, skill name, publisher, version, target agent, and install command before approving installation. <br>
Risk: Using an automatic npx fallback can execute the latest published CLI package instead of a locally trusted installation. <br>
Mitigation: Prefer a trusted global reskill installation and use npx only when that fallback is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krislavten/rush-find-skills) <br>
- [reskill package manager](https://github.com/nicepkg/reskill) <br>
- [Rush registry](https://rush.zhenguanyu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill presents search results and install commands, and asks for user confirmation before installation.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
