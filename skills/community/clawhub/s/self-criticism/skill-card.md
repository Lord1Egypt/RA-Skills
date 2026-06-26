## Description: <br>
Insert breakpoint self-critique before branching work, after user friction, and at risky handoffs so agents catch errors early. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent builders, and external users use this skill to add lightweight self-critique at inflection points before plans branch, commitments become expensive, or user friction reveals process drift. It helps agents choose critique depth, keep local trigger memory, and update small workspace steering files when the user approves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent self-critique memory can capture sensitive personal or project details if used too broadly. <br>
Mitigation: Keep saved notes limited to process lessons, critique triggers, and depth preferences; avoid storing private details unrelated to critique timing or quality control. <br>
Risk: Workspace integration may modify main memory, ~/self-criticism/, AGENTS.md, or SOUL.md. <br>
Mitigation: Review proposed writes before execution and require explicit session approval before changing workspace steering files. <br>
Risk: Overuse can slow work or turn critique into noisy ritual. <br>
Mitigation: Use the lightest critique depth that can catch the likely failure, and trigger it mainly before branching, commitment, surprising evidence, user friction, or risky handoffs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/self-criticism) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>
- [Skill homepage](https://clawic.com/skills/self-criticism) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces breakpoint questions, critique depth guidance, local memory templates, and optional workspace integration snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
