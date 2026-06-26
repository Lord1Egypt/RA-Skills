## Description: <br>
Self-Governor adds a lightweight decision layer that asks an agent to choose one next action at branching points, before costly or irreversible steps, or after stalled progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z1one0415](https://clawhub.ai/user/z1one0415) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to help an agent choose a single next action from a fixed action set during multi-step strategy, research, coding, search, and workflow tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can steer an agent to continue around costly or irreversible actions without requiring user confirmation. <br>
Mitigation: Require explicit user confirmation before any tool call that publishes, deletes, overwrites, modifies accounts, or spends credits. <br>


## Reference(s): <br>
- [Actions Reference](references/actions.md) <br>
- [Examples Reference](references/examples.md) <br>
- [Input-Output Reference](references/input-output.md) <br>
- [Triggers Reference](references/triggers.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Structured JSON-like fields with one next_action, a short reason, and an optional fallback_if_fail] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns exactly one action selected from anchor, time_bind, search, clean, synthesize, or degrade_continue.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
