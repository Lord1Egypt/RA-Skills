## Description: <br>
Manage and maintain the local Agent Control UI with reliable caching, dashboards, tabs, and conflict-free server handling on port 8765. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[motivationationdaily](https://clawhub.ai/user/motivationationdaily) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to maintain a local Agent Control UI, including stale UI state, dashboard and tab updates, resilient endpoints, and port 8765 conflicts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Port 8765 cleanup could affect an unrelated local service. <br>
Mitigation: Confirm the listener belongs to the intended Agent Control UI before stopping or replacing it. <br>
Risk: UI maintenance changes could touch the wrong local files or leave stale state visible. <br>
Mitigation: Confirm the intended UI files before editing and add cache-busting for static assets when state freshness matters. <br>
Risk: Heavy local work could block the UI server event loop. <br>
Mitigation: Run expensive work in threads and keep endpoints resilient to missing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/motivationationdaily/ui-control-center) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with code edits and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local server checks, endpoint changes, cache-busting updates, and action logging guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
