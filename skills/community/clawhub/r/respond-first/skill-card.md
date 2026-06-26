## Description: <br>
Multi-agent dispatcher skill where the main agent acts as a coordinator that chats with users and delegates work to five persistent sub-agent sessions through round-robin scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Be1Human](https://clawhub.ai/user/Be1Human) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to route task requests through a coordinator that replies to the user first, then delegates the actual work to one of five persistent sub-agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User requests may include secrets or unrelated private information that would be delegated to persistent sub-agent sessions. <br>
Mitigation: Provide only task-relevant context and avoid secrets unless delegation and possible retention in those sessions are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Be1Human/respond-first) <br>
- [Publisher profile](https://clawhub.ai/user/Be1Human) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, API Calls] <br>
**Output Format:** [Plain text responses with structured sessions_spawn calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Delegates task context to one of five fixed sessionKeys with a 300-second run timeout when spawning sub-agent work.] <br>

## Skill Version(s): <br>
11.0.0 (source: SKILL.md frontmatter, skill.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
