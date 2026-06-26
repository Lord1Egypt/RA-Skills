## Description: <br>
Logs trades with full context, generates weekly and monthly performance reports, and helps identify patterns in wins, losses, emotions, and strategy updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and trading-system builders use this skill to maintain a structured local trade journal, review weekly or monthly performance, and refine strategy rules from logged outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local journal can contain sensitive trade history, PnL, strategy notes, and emotion labels. <br>
Mitigation: Keep the journal private, avoid synced or shared workspaces unless intended, and review file contents before sharing logs or reports. <br>
Risk: Generated strategy adjustments or trading-system updates may be incomplete, incorrect, or unsuitable for the user's risk tolerance. <br>
Mitigation: Manually review and approve any suggested strategy or trading-system change before applying it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-trading-journal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON trade-record examples and report summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or updates a local trading journal file at ~/.openclaw/workspace/trading/journal.json when the agent follows the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
