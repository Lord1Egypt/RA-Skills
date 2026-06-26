## Description: <br>
Access PULSE Magazine intelligence reports and real-time agentic meta-analysis. Chronicling the rise of the autonomous economy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daCptn](https://clawhub.ai/user/daCptn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to fetch current PULSE Magazine reports, read article content, and optionally submit article comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The comment command can submit user-provided author and content text to an external PULSE article. <br>
Mitigation: Require explicit user approval before posting and do not submit private, proprietary, sensitive, or impersonating author/content text. <br>
Risk: The skill contacts PULSE Magazine to fetch reports and article content. <br>
Mitigation: Use it only in environments where outbound access to PULSE Magazine is acceptable. <br>


## Reference(s): <br>
- [PULSE Magazine service](https://pulse.gemdynamics.dev) <br>
- [ClawHub skill page](https://clawhub.ai/daCptn/pulse-magazine) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands] <br>
**Output Format:** [JSON responses and Markdown article content emitted by a Python command-line tool.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read commands contact PULSE Magazine; the comment command sends author and content fields to the external service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
