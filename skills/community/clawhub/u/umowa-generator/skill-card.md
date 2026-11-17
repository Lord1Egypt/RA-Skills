## Description:

UmowaGenerator helps users in Poland generate Polish legal contract templates for common agreements such as service, work-for-hire, rental, preliminary purchase, and vehicle sale contracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomasz-pedzierski-infinity](https://clawhub.ai/user/tomasz-pedzierski-infinity)

### License/Terms of Use:

MIT-0

## Use Case:

External users, individuals, and small businesses in Poland use this skill to draft contract templates by providing party details, agreement type, subject matter, compensation, and dates. The generated documents should be treated as templates for review rather than legal advice.

### Deployment Geography for Use:

Poland

## Known Risks and Mitigations:

Risk: Generated contracts may be mistaken for legal advice or final legally sufficient documents.

Mitigation: Treat generated contracts as templates and have a qualified reviewer validate them before relying on them.

Risk: The workflow asks for personal identifiers and address data, including PESEL, NIP, names, and residential addresses.

Mitigation: Minimize personal data entered into prompts, avoid unnecessary sharing, and handle generated documents according to applicable privacy requirements.

Risk: The reviewed artifact advertises PRO PDF and email capabilities without evidence of a secure implemented workflow.

Mitigation: Verify PDF or email handling separately before using those features for sensitive contracts.

Risk: Several command-line paths appear broken according to the security review guidance.

Mitigation: Run local tests and manually review generated output before relying on command-line results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomasz-pedzierski-infinity/skills/umowa-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/tomasz-pedzierski-infinity)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact generator script](artifact/umowa_generator.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown and plain text contract-template content, with optional Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated content may include Polish personal-data fields such as PESEL, NIP, names, and addresses.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact script header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
