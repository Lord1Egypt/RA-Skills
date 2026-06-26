## Description: <br>
Guides agents through code review feedback by verifying suggestions, asking for clarification, and implementing changes only after technical evaluation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenleiyanquan](https://clawhub.ai/user/chenleiyanquan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use this skill when receiving code review feedback to verify suggestions, clarify unclear items, push back on incorrect advice, and implement accepted changes with tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead the agent to inspect project files while evaluating review feedback. <br>
Mitigation: Use it only in workspaces where the agent is allowed to read review-relevant project files. <br>
Risk: The skill may suggest GitHub CLI or API commands that post, edit, or mutate pull request content. <br>
Mitigation: Review any gh api command before execution and confirm the repository, pull request, and comment identifiers. <br>
Risk: Ambiguous review feedback can still result in incorrect code changes if acted on too early. <br>
Mitigation: Clarify unclear review items before implementation and run targeted tests after accepted changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenleiyanquan/receiving-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, shell commands] <br>
**Output Format:** [Markdown or plain text with optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May suggest GitHub CLI or API commands for review-thread replies; no external service credentials are declared by the skill itself.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
