## Description: <br>
Files, sockets, subscriptions, or other finite resources are acquired without a guaranteed release path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvogt99](https://clawhub.ai/user/mvogt99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to help an agent recognize resource leaks in code and suggest reliable acquire/release patterns for files, sockets, database or HTTP clients, event listeners, background tasks, and timers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The surrounding agent may inspect repository files while applying this resource-leak guidance. <br>
Mitigation: Grant the agent access only to repositories and files that are intended for analysis. <br>
Risk: Resource-management advice may be incomplete or mismatched to a specific language, framework, or runtime. <br>
Mitigation: Review proposed changes and test teardown and error paths before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown prose with bullet-point findings and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text-only helper; does not run code or request sensitive access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
