## Description: <br>
Generate, fetch, poll, and clear disposable email addresses using the Vortex API for temporary inboxes during signup or testing flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[techwithanirudh](https://clawhub.ai/user/techwithanirudh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and QA testers use this skill to create disposable inboxes, poll or fetch messages, and clear temporary mail during signup or testing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Temporary mailbox contents are handled by a third-party hosted service. <br>
Mitigation: Use the skill only for low-risk signup or testing workflows, and avoid sensitive personal, financial, production, account-recovery, or secret-bearing email. <br>
Risk: The clear command empties the selected temporary mailbox. <br>
Mitigation: Double-check the email address before clearing mailbox contents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/techwithanirudh/temp-mail) <br>
- [Vortex homepage](https://vortex.skyfall.dev) <br>
- [Vortex API endpoint](https://vtx-api.skyfall.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Plain text, JSON API responses, and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.11+ and Python dependencies for the bundled CLI; mailbox operations call the hosted Vortex API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
