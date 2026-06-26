## Description: <br>
Scrask parses screenshots from chat surfaces for events and tasks, emits structured intent JSON, and lets the OpenClaw agent route calendar or task creation to installed destination skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devsandip](https://clawhub.ai/user/devsandip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Scrask to turn screenshots of invitations, deadlines, bookings, and chat messages into calendar events or task-list items through their configured OpenClaw assistant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots may contain private chats, credentials, medical, financial, or work-confidential information and can be sent to the configured vision provider or optional Gemini/Claude providers. <br>
Mitigation: Review provider configuration before installing, avoid sensitive screenshots, and limit use to screenshots the user is comfortable sending to the configured model provider. <br>
Risk: Calendar or task entries may be created without a final approval step when extracted fields pass the configured confidence thresholds. <br>
Mitigation: Require explicit confirmation before dispatching writes, tune confidence thresholds conservatively, or disable broad implicit routing for high-sensitivity users. <br>


## Reference(s): <br>
- [Scrask ClawHub Release](https://clawhub.ai/devsandip/scrask-bot) <br>
- [Publisher Profile](https://clawhub.ai/user/devsandip) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Architecture Overview](artifact/docs/ARCHITECTURE_OVERVIEW.md) <br>
- [Decision Flow](artifact/docs/decision-flow.md) <br>
- [Example Walkthrough](artifact/docs/example-walkthrough.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown/chat text, JSON intent objects, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Parser output includes confidence scores, clarification prompts, routing destinations, and summary text for the agent to relay.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact SKILL.md and CHANGELOG report 4.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
