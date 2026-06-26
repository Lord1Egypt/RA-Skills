## Description: <br>
Minimal CLI for the Toss Payments Core API to retrieve payment details and perform full or partial payment cancellations with payment keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to work with Toss Payments from the command line, including payment lookup and full or partial cancellation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cancel real Toss Payments transactions when provided a valid secret key. <br>
Mitigation: Use test keys first, require explicit human confirmation before cancellation, and restrict production keys as much as Toss Payments allows. <br>
Risk: The skill depends on TOSS_SECRET_KEY and allows the base URL to be overridden. <br>
Mitigation: Store the secret key securely, avoid exposing it in logs, and keep TOSS_BASE_URL pointed at trusted Toss Payments endpoints. <br>


## Reference(s): <br>
- [Toss Payments Core API](https://docs.tosspayments.com/reference#tag/Payments) <br>
- [ClawHub Skill Page](https://clawhub.ai/chloepark85/toss-payments-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that retrieve payment details or cancel Toss Payments transactions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
