## Description: <br>
Example TaskFlow authoring pattern for inbox triage. Use when messages need different treatment based on intent, with some routes notifying immediately, some waiting on outside answers, and others rolling into a later summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1yihui](https://clawhub.ai/user/1yihui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent authors use this skill as a TaskFlow pattern for routing inbox items into business, personal, and end-of-day summary paths while preserving flow state and waiting only when outside input is required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Inbox routing can send items to the wrong Slack destination or notify the wrong audience if adapted without review. <br>
Mitigation: Confirm Slack destinations and notification approval before deployment. <br>
Risk: Persisted inbox state may retain more message data than necessary. <br>
Mitigation: Store only the minimal routing state needed for the active batch. <br>
Risk: Detached classification tasks can become hard to monitor if they are left unbounded. <br>
Mitigation: Keep classification tasks bounded and visible when adapting the pattern. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1yihui/taskflow-inbox-triage) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with TypeScript and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance for TaskFlow inbox routing; no executable code is packaged.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
