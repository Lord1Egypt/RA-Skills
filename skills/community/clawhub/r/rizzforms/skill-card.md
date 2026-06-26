## Description: <br>
Create forms, configure webhook delivery, manage submissions, and generate embed HTML using the RizzForms API and bundled CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blairanderson](https://clawhub.ai/user/blairanderson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site owners use this skill to add contact, feedback, signup, lead capture, or waitlist forms that collect submissions through RizzForms and optionally deliver them to webhook endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Form submissions may be routed to an external hosted backend and webhook destination. <br>
Mitigation: Use this skill only when RizzForms or another hosted form backend is intended; confirm webhook destinations and avoid collecting secrets or regulated data without appropriate disclosures and consent. <br>
Risk: The workflow can require admin-level API credentials to create forms, manage webhooks, and read submissions. <br>
Mitigation: Use the least-privileged API key available, keep API keys out of source code, and rotate keys or webhook signing secrets when access changes. <br>
Risk: The artifact describes a bundled CLI, but the provided package evidence only includes the skill instructions and API reference. <br>
Mitigation: Confirm the CLI is actually present before relying on CLI-only commands; otherwise use the documented API behavior as the source of truth. <br>


## Reference(s): <br>
- [RizzForms API Reference](references/api.md) <br>
- [RizzForms API and Dashboard](https://www.rizzness.com) <br>
- [RizzForms Signup](https://forms.rizzness.com/signup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell, HTML, JSON, and framework code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include form endpoint tokens, webhook configuration steps, embed HTML, API command guidance, and submission-management instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
