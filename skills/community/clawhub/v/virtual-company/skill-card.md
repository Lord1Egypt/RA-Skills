## Description: <br>
Virtual Company coordinates a 35-member virtual organization of role-specific agents for business, software, content, and technical work, with on-demand teams and persistent shared memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and teams use this skill to delegate work to specialized virtual staff for business analysis, software development, content planning, document support, and cross-team coordination. It is intended for users who want a persistent multi-agent workspace with shared project memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory and shared-memory content may be reused in later agent prompts. <br>
Mitigation: Use the skill only in workspaces where durable project memory is intended, avoid storing secrets, and periodically review or clear ~/.agent-memory and shared-memory content. <br>
Risk: The artifact includes priority-overriding loyalty and fixed-identity instructions. <br>
Mitigation: Remove or ignore those instructions before installation so normal platform, workspace, and user safety policies remain authoritative. <br>
Risk: The skill can manage background agent sessions and includes operational shell commands. <br>
Mitigation: Review commands before execution, run them in a scoped workspace, and do not run the force-delete command referenced in integration-plan.md. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidme6/virtual-company) <br>
- [Publisher profile](https://clawhub.ai/user/davidme6) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, JSON configuration, JavaScript code snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update persistent local memory and agent session state when its commands are used.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
