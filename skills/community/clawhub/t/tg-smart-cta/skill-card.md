## Description: <br>
Enhances Telegram replies with context-aware dynamic CTA buttons that provide relevant, time-sensitive, and task-oriented options for better interaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dendyadinirwana](https://clawhub.ai/user/dendyadinirwana) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents replying on Telegram use this skill to suggest quick-action buttons that match the user's context, task stage, and time of day while keeping manual input available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proactive CTA buttons may steer users toward actions they did not request. <br>
Mitigation: Review button suggestions for task fit and always include a manual input option so users can choose their own next step. <br>
Risk: Generic or overlapping callback_data values may be ambiguous in a Telegram bot backend. <br>
Mitigation: Prefer strict callback routing and namespaced callback IDs when deploying the Telegram bot backend. <br>


## Reference(s): <br>
- [Time-Based Button Presets](references/time_logic.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript-style message button examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces suggested Telegram button rows, button labels, and callback_data values for agent replies.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
