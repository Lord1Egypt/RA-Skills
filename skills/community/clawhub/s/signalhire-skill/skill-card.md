## Description:

The SignalHire skill guides agents in using the SignalHire API to search professional profiles and companies, enrich contact details, and handle asynchronous callback-based results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nts](https://clawhub.ai/user/nts)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search for prospects or companies and request contact enrichment through SignalHire. It is intended for workflows that have a legitimate SignalHire account and a lawful basis for handling personal contact data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles personal contact data returned by SignalHire.

Mitigation: Use it only with a legitimate SignalHire account and a lawful basis for contact lookup, and avoid unnecessary storage or sharing of enrichment results.

Risk: Callback-based enrichment can expose webhook endpoints and callback secrets.

Mitigation: Prefer a presecured callback service, validate shared secrets, use HTTPS, and rotate callback secrets when exposure is suspected.

Risk: API keys and callback URLs may be exposed through shell commands, logs, or command history.

Mitigation: Keep credentials in environment variables or a managed secret store and avoid echoing sensitive values into logs or persistent command history.

## Reference(s):

- [ClawHub SignalHire Skill Page](https://clawhub.ai/nts/skills/signalhire-skill)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline Python, shell, and environment configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request instructions, callback setup steps, status handling guidance, and notes about remaining credits.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
