## Description: <br>
Talent advisor skill for AI agents that helps users clarify career direction, optimize profiles, discover opportunities, apply strategically, and communicate with employers through Coffee Shop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jblue-ops](https://clawhub.ai/user/jblue-ops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to run a job search: build and sync a career profile, search for roles, submit applications, track status, and reply to employer messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle sensitive job-search data and sync profile, application, and message data through Coffee Shop. <br>
Mitigation: Review what will be stored or synced, avoid sharing sensitive PII, and require explicit approval before profile syncs. <br>
Risk: The skill can submit applications and send recruiter messages on the user's behalf. <br>
Mitigation: Require the agent to show each application, profile change, and outbound message for user approval before sending. <br>
Risk: The artifact recommends a remote curl-to-bash installer. <br>
Mitigation: Prefer manual or otherwise verifiable installation paths, and inspect any remote installer before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jblue-ops/talentclaw) <br>
- [Talentclaw Homepage](https://github.com/artemyshq/talentclaw) <br>
- [Coffee Shop CLI Package](https://www.npmjs.com/package/@artemyshq/coffeeshop) <br>
- [Application Playbook](references/APPLICATION-PLAYBOOK.md) <br>
- [Career Strategy Guide](references/CAREER-STRATEGY.md) <br>
- [Profile Optimization Guide](references/PROFILE-OPTIMIZATION.md) <br>
- [Tool & CLI Reference](references/TOOLS.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline CLI commands and JSON/TOML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local career files and use Coffee Shop CLI/MCP workflows for profile, application, and messaging tasks.] <br>

## Skill Version(s): <br>
2.2.0 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
