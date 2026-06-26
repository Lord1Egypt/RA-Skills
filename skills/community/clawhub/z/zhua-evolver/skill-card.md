## Description: <br>
Zhua Evolver helps an agent analyze capability gaps, search for supplemental skills, run evolution cycles, record changes, and coordinate helper roles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beipian261](https://clawhub.ai/user/beipian261) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to plan and run capability-improvement workflows, including gap analysis, skill discovery, installation planning, evolution logging, and role-based task coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to expand and change its own capabilities without enough approval controls. <br>
Mitigation: Use only under close supervision and require explicit review before skill searches, installations, configuration changes, or continuous evolution steps. <br>
Risk: Automatic installation, identity-file edits, or rollback-prevention behavior could create changes that are difficult to audit or undo. <br>
Mitigation: Allow changes only when each action is shown first, sourced from a trusted registry, and paired with an easy rollback path. <br>


## Reference(s): <br>
- [Reference Documentation for Zhua Evolver](references/api_reference.md) <br>
- [Zhua Evolver ClawHub Release](https://clawhub.ai/beipian261/zhua-evolver) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, code snippets, and structured text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce JSON from helper scripts when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
