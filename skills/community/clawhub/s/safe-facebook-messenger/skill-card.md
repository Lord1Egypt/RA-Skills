## Description: <br>
Safe Facebook Messenger helps an agent send or draft Facebook Messenger messages through a signed-in Chrome session using Chrome DevTools MCP with thread verification, composer checks, search reacquisition, group-chat disambiguation, social-risk screening, and verified send or draft workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TSchonleber](https://clawhub.ai/user/TSchonleber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using an agent with Chrome DevTools MCP use this skill to safely send or draft Facebook Messenger messages in a signed-in browser session while reducing misdirected messages and risky sends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent operates a signed-in Messenger browser session and may inspect visible conversation state. <br>
Mitigation: Use a deliberately selected Chrome profile, supervise sends, and review any Chrome DevTools MCP or runtime logging settings before use. <br>
Risk: A message could be drafted or sent to the wrong thread if Messenger UI state is stale or ambiguous. <br>
Mitigation: Verify the active conversation, composer ownership, draft placement, and send result with fresh browser state; stop on ambiguity instead of guessing. <br>
Risk: Sensitive or high-consequence messages could create social, financial, legal, or professional exposure. <br>
Mitigation: Prefer drafts or escalation for sensitive content, commitments, money, deadlines, legal issues, first outreach, and other messages likely to need review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TSchonleber/safe-facebook-messenger) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow for browser-based Messenger drafting and sending; the skill itself does not produce files or code.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
