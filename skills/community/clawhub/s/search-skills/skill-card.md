## Description: <br>
Helps users discover and install agent skills when they ask questions like "how do I do X", "search a skill for X", "is there a skill that can...", or express interest in extending capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlang-cn](https://clawhub.ai/user/openlang-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find relevant installable skills for specialized tasks, compare options, and receive skill search or installation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may recommend or install third-party skills that have not been reviewed by the user. <br>
Mitigation: Review the skill, publisher, and installation target before installing. <br>
Risk: The documented global install command uses `-y`, which skips confirmation prompts and can affect future agent sessions. <br>
Mitigation: Use confirmation prompts by default, avoid `-y` unless intentional, and use global installs only when persistent availability is required. <br>


## Reference(s): <br>
- [Skills directory](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include third-party skill installation commands; review the skill and publisher before installing.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
