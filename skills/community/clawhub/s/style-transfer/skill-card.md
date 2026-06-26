## Description: <br>
Extracts a target website's design system and applies it to Vue, React, Next.js, and Tailwind projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[babywhale](https://clawhub.ai/user/babywhale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to transfer the visual language of a reference website into an existing frontend project. It guides extraction of design tokens and integration into Vue, React, Next.js, Tailwind, or plain CSS workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to edit local frontend source files. <br>
Mitigation: Review generated diffs before committing or deploying changes. <br>
Risk: The skill may run normal development commands such as package scripts or builds in the target project. <br>
Mitigation: Use it only in projects where running local development commands is acceptable, especially when the repository is unfamiliar. <br>
Risk: Transferred styles may introduce incorrect visual changes or integration problems. <br>
Mitigation: Run the project's build or dev verification commands and inspect the resulting UI before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/babywhale/style-transfer) <br>
- [Publisher profile](https://clawhub.ai/user/babywhale) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include project-specific file edits and verification commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
