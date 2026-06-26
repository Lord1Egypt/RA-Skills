## Description: <br>
双脑调度核心 coordinates multi-skill tasks by routing work, passing context, arbitrating Executor/Critic conflicts, handling errors, and returning structured decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to coordinate complex multi-skill workflows that need context envelopes, critic review, arbitration, retries, and fallback handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The orchestrator can pass prior outputs, critic insight, and analysis to downstream skills, so unnecessary sensitive or unrelated context could be shared. <br>
Mitigation: Limit the input context to data downstream skills genuinely need, and keep credentials, private files, and unrelated prior outputs out of the envelope. <br>
Risk: Complex orchestration decisions can route work to fallback or retry paths that may still need human review for correctness. <br>
Mitigation: Review final orchestration outputs before acting on them, especially when fallback is used or critic confidence is low. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, json, text] <br>
**Output Format:** [Structured JSON object with orchestration status, decisions, critic insight, arbitration details, next action, data envelope, and retry count.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains a fixed output structure even when some fields are not applicable.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
