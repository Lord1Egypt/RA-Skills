## Description: <br>
Discard the accumulated drafts and framings from this thread and re-derive the task from a clean problem statement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Agents and users use this skill when a conversation has been anchored by earlier drafts and needs a clean factual brief, a fresh derivation, or a handoff to a fresh context for deep or high-stakes contamination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to discard useful task history, prior risk decisions, or safety-relevant constraints if invoked at the wrong time. <br>
Mitigation: Use it only when an explicit context reset or clean re-derivation is desired, and preserve hard constraints, known facts, ruled-out attempts, and prior safety decisions in the extracted brief. <br>
Risk: A contaminated in-thread model may not be reliable enough to reset its own reasoning for deep contamination or high-stakes work. <br>
Mitigation: For deep contamination or high-stakes cases, hand the extracted brief to a fresh subagent or start a new session instead of re-deriving in the same thread. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/reset-context-contamination) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown or plain text brief with recommended next action] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend a fresh session or subagent for deep contamination and high-stakes work.] <br>

## Skill Version(s): <br>
0.1.0 (source: skill metadata and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
