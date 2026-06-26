## Description: <br>
Run real user interviews via Usercall when qualitative feedback is needed for onboarding drop-off, feature confusion, pricing clarity, prototype testing, or similar research questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junetic](https://clawhub.ai/user/junetic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product teams, researchers, founders, and developers use this skill to create Usercall interview studies, share participant links, check study status, add participant slots, and summarize interview results with themes and quotes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to check the Usercall API key in a way that can print the secret into the terminal or logs. <br>
Mitigation: Use a non-printing key presence check and avoid exposing the value in command output. <br>
Risk: The skill may send research goals, business context, customer details, prototype links, or images to Usercall. <br>
Mitigation: Confirm that the study content and linked materials are intended to be shared with Usercall before creating the study. <br>
Risk: Persisting the API key in shell startup files can broaden credential exposure. <br>
Mitigation: Prefer a session-scoped environment variable or a secret manager for the Usercall API key. <br>


## Reference(s): <br>
- [Usercall](https://app.usercall.co) <br>
- [ClawHub release page](https://clawhub.ai/junetic/user-interview) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Usercall study links, status responses, and summarized interview themes with quotes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
