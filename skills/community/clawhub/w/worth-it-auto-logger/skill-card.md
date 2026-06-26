## Description: <br>
Automatically detects active projects, tracks session time, captures value signals and costs during conversations, and summarizes ROI through Worth It. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[storyscriptapp](https://clawhub.ai/user/storyscriptapp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who already run Worth It use this skill to let an agent automatically capture ROI signals, session time, and API or tool costs across conversations, then batch those records to Worth It for ROI summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Silent monitoring can create inferred financial or productivity records without clear per-session user consent. <br>
Mitigation: Enable only when the user intentionally wants auto-logging, disclose the behavior, and confirm how auto-logging can be disabled before use. <br>
Risk: Conversation-derived ROI, time-saved, and cost estimates may be inaccurate or double-counted. <br>
Mitigation: Use the configured confidence threshold, avoid duplicate signals, and ensure users can inspect, edit, or delete automatically created entries. <br>
Risk: Conversation context and financial or productivity metadata may be stored by Worth It. <br>
Mitigation: Confirm where records are stored, who can access them, and what retention or deletion controls are available before enabling the skill. <br>


## Reference(s): <br>
- [Worth It Auto-Logger on ClawHub](https://clawhub.ai/storyscriptapp/worth-it-auto-logger) <br>
- [Worth It - Agent Profitability Tracker on ClawMart](https://www.shopclawmart.com/listings/worth-it-agent-profitability-tracker-961a92fb) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples, HTTP API calls, shell commands, and brief text updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Batches ROI signals at session end and may emit a short Worth It update when meaningful value is logged.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, created 2026-03-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
