## Description: <br>
Use when an agent needs Dreamina（即梦） image or video generation through the Dreamina CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l1angjy](https://clawhub.ai/user/l1angjy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect Dreamina CLI help, submit image or video generation tasks, check account credits, and query async results. It is intended for workflows where the user can review commands before credit-spending or account-affecting actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or running the Dreamina CLI requires trusting the Dreamina/Jianying source and may use a logged-in account. <br>
Mitigation: Install only from the documented source, reuse existing login state unless the user requests an account action, and show the exact command before execution. <br>
Risk: Submitting generation jobs can consume account credits and may expose prior task history during result checks. <br>
Mitigation: Confirm any credit-spending action with the user, separate help-only inspection from real submissions, and query only task IDs or history the user approves. <br>


## Reference(s): <br>
- [Dreamina CLI installer](https://jimeng.jianying.com/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and CLI result guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Dreamina submit_id values, generation status checks, and follow-up query commands.] <br>

## Skill Version(s): <br>
2026.4.10-1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
