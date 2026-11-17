## Description:

Automates Twitter/X operations for @Gsdata5566, including following back verified followers and new followers, drafting deeper comments, and posting friendly growth-oriented replies through a user-authenticated X web session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:

MIT-0

## Use Case:

Social media operators and account owners use this skill to automate routine Twitter/X engagement tasks for a specific logged-in account, including follow-backs and short public replies. It is intended for controlled account operations where the user has intentionally logged in and authorized the session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can follow accounts or post replies from whichever X account is currently logged into the browser session.

Mitigation: Verify the active account before each run and use it only with an account the user intentionally authenticated for this purpose.

Risk: Immediate follow-back automation may create unwanted follows or exceed the user's intended scope.

Mitigation: Require explicit confirmation, set conservative per-run limits, and review target lists before executing follow-back commands.

Risk: Public replies may be posted without adequate review.

Mitigation: Preview and approve every reply draft before posting, and avoid repetitive or promotional text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kelcey2023/skills/zeelin-twitter-x-autopost)
- [Target X account](https://x.com/Gsdata5566)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and short status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces public-reply drafts and command-oriented browser automation steps for an authenticated X session.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
