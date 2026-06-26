## Description: <br>
Manage enterprise SSO, Directory Sync (SCIM), Admin Portal links, and user management through the WorkOS API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dwhite-oss](https://clawhub.ai/user/dwhite-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators use this skill to generate WorkOS API calls for organization setup, SSO connection checks, Directory Sync queries, Admin Portal link creation, and AuthKit user management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide privileged WorkOS administration with a sensitive API key. <br>
Mitigation: Install only when the agent is expected to administer WorkOS, protect WORKOS_API_KEY, and scope access according to operational need. <br>
Risk: The skill includes high-impact user deletion instructions. <br>
Mitigation: Require explicit confirmation before create or delete operations and carefully verify organization and user IDs before execution. <br>


## Reference(s): <br>
- [WorkOS API](https://api.workos.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/dwhite-oss/workos) <br>
- [Publisher Profile](https://clawhub.ai/user/dwhite-oss) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a WORKOS_API_KEY environment variable for generated API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
