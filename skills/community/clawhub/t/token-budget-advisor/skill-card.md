## Description: <br>
Offer users informed choice about response depth before answering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to choose response depth before the agent answers when they mention token budget, token usage, response length, or similar constraints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may pause to ask for a preferred answer depth when token-budget trigger wording appears. <br>
Mitigation: Narrow the trigger wording before use if these activations would interrupt normal workflows. <br>
Risk: Token counts are heuristic estimates and may differ from actual model tokenization. <br>
Mitigation: Treat the estimates as planning guidance rather than exact budget accounting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/djc00p/token-budget-advisor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text] <br>
**Output Format:** [Markdown or plain text with token estimates and numbered depth choices] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Heuristic token estimates; no real tokenizer.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
