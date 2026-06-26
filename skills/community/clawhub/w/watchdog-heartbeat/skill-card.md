## Description: <br>
Monitor service health, heartbeat freshness, stuck workflows, and trigger recovery or degraded mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunbinnju-star](https://clawhub.ai/user/sunbinnju-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review service health, heartbeat freshness, and workflow progress in a resident OpenClaw system, then identify recovery or degraded-mode recommendations when issues appear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may surface service health data, heartbeat history, and workflow status that could be sensitive in production environments. <br>
Mitigation: Install only where sharing that operational data is acceptable and keep the monitored service list scoped. <br>
Risk: Recovery recommendations such as restarts or degraded-mode changes could affect availability if executed automatically without review. <br>
Mitigation: Require explicit human or policy approval before separate automation performs restarts or degraded-mode changes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Configuration] <br>
**Output Format:** [Structured text with JSON-like report sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces service health summaries, expired heartbeat lists, stuck workflow lists, recovery recommendations, degraded-mode recommendations, and watchdog logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
