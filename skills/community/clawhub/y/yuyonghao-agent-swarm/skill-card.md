## Description: <br>
Agent Swarm provides an in-memory JavaScript coordinator for creating agent swarms, registering agents, distributing tasks, and checking swarm status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to prototype multi-agent coordination flows with swarm lifecycle management, agent registration, task distribution, and status monitoring. It is most suitable for local or embedded coordination experiments that need a lightweight JavaScript API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation describes TaskSharder, SelfOrganizer, EmergentBehavior, and SwarmMonitor modules that are not included in the artifact. <br>
Mitigation: Review the exported API before relying on documented modules; the artifact exports SwarmCoordinator only. <br>
Risk: The release is a small in-memory coordination library, so production readiness depends on caller-side validation, persistence, authorization, and operational controls. <br>
Mitigation: Wrap the coordinator with application-specific access control, input validation, monitoring, and durable state if using it beyond local prototyping. <br>


## Reference(s): <br>
- [Agent Swarm ClawHub listing](https://clawhub.ai/yuyonghao-123/yuyonghao-agent-swarm) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [JavaScript module exports, examples, and JSON-like task and status objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs in memory; no network, credential, filesystem, persistence, or privilege behavior is reported by the security evidence.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
