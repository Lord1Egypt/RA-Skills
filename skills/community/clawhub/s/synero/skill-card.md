## Description: <br>
Ask Synero's AI Council questions from the terminal and get one synthesized answer from four contrasting AI advisors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blovett80](https://clawhub.ai/user/blovett80) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and other users can ask Synero judgment-heavy questions about strategy, research, architecture, hiring, positioning, or similar decisions where multiple perspectives and a final synthesis are useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, thread IDs, and parent query IDs may be sent to Synero's remote API. <br>
Mitigation: Avoid secrets, personal data, customer data, regulated information, and proprietary source code unless use of Synero is approved for that data. <br>
Risk: A custom SYNERO_API_URL can redirect requests and prompt data to a configured endpoint. <br>
Mitigation: Only set SYNERO_API_URL to an endpoint you trust, and use a revocable API key. <br>
Risk: Synthesized AI recommendations can still be incomplete or unsuitable for high-impact decisions. <br>
Mitigation: Review the synthesis against the user's constraints, available evidence, and domain requirements before acting on it. <br>


## Reference(s): <br>
- [Prompt Patterns](references/prompt-patterns.md) <br>
- [Synero](https://synero.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/blovett80/synero) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal text or Markdown; raw Server-Sent Events are available in debugging mode.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and SYNERO_API_KEY; optional environment variables can override the API URL, timeout, advisor models, and synthesizer model.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
