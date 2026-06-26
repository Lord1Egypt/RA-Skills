## Description: <br>
Team collaboration system for managing projects, requirements, tasks, bugs, documents, milestones, discussions, notifications, roles, and permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magieSky](https://clawhub.ai/user/magieSky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team operations agents use this skill to work with a local team collaboration backend for project planning, requirements management, task tracking, bug tracking, document records, milestones, discussions, notifications, and role or permission data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports reusable credentials and a fixed API key in the skill documentation. <br>
Mitigation: Rotate or remove documented credentials before use, configure least-privilege authentication, and avoid exposing the local backend outside a trusted environment. <br>
Risk: The skill exposes delete operations and role or permission management actions that can change project records or access controls. <br>
Mitigation: Require manual approval for delete, role, and permission changes, and test against non-production data before connecting to shared or production systems. <br>
Risk: The security review recommends trusted local test use unless the backend has strong server-side authorization. <br>
Mitigation: Verify backend authorization and audit logging before broader deployment, and limit installation to trusted local setups until those controls are confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/magieSky/team-collaboration) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON or string responses from local HTTP API actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local backend at http://localhost:8080; most actions require bearer-token or API-key authentication.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact metadata reports 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
