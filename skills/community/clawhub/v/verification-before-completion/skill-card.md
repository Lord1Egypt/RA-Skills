## Description: <br>
Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlc000190](https://clawhub.ai/user/zlc000190) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to require fresh verification evidence before an agent claims work is complete, fixed, passing, or ready for commit or PR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification commands may be slow, expensive, or have side effects in some environments. <br>
Mitigation: Tell the agent which verification commands are appropriate and flag commands that should not be run automatically. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlc000190/verification-before-completion) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text] <br>
**Output Format:** [Markdown or plain text with verification command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May prompt the agent to run tests, builds, linters, or comparable verification commands before reporting completion.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
