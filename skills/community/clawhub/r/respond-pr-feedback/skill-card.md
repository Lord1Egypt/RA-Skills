## Description: <br>
Respond to review comments on a PR after evaluation and fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill after evaluating pull request review feedback to post concise replies to unreplied GitHub review comments and optionally resolve the related review threads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post PR review replies and resolve review threads through the user's GitHub identity. <br>
Mitigation: Review queued comments and proposed responses before use, and pass --no-resolve when conversations should remain open. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/respond-pr-feedback) <br>
- [Publisher profile](https://clawhub.ai/user/anderskev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown summary with GitHub CLI commands and concise PR review replies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May post GitHub review comment replies and resolve review threads unless --no-resolve is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
