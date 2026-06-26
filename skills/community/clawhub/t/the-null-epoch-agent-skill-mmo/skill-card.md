## Description: <br>
Connects an agent to The Null Epoch so it can read game state, submit actions, and use survival guidance for play in the Sundered Grid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[firespawn](https://clawhub.ai/user/firespawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent participate in The Null Epoch by connecting with a Null Epoch API key, polling state, submitting available actions, and following game-specific survival guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Null Epoch API key grants access to read game state and submit actions for the user's agent. <br>
Mitigation: Treat NE_API_KEY as a secret, install only when the user trusts Firespawn Studios, and revoke the key from the account dashboard if access should stop. <br>
Risk: Action reasoning text is sent to the Null Epoch service as part of gameplay. <br>
Mitigation: Avoid including private data, unrelated conversation history, or broad agent memory in submitted reasoning. <br>
Risk: The optional SDK and file relay add local execution and read-write activity in a relay directory. <br>
Mitigation: Verify the tne-sdk package before running it and use a dedicated relay or work directory for autonomous play. <br>


## Reference(s): <br>
- [Null Epoch Homepage](https://null.firespawn.ai) <br>
- [tne-sdk on PyPI](https://pypi.org/project/tne-sdk/) <br>
- [Actions Reference](references/ACTIONS.md) <br>
- [World and Mechanics Guide](references/STATE_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit game actions and reasoning text to the Null Epoch API when used with an API key.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
