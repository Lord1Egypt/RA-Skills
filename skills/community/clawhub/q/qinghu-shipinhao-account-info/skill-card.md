## Description:

Looks up WeChat Channels account location and verification details, including certified entity, entity type, service category, and certification date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents can retrieve the published verification and location information for a specified WeChat Channels account to identify its certified operator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party CLI and Qinghu service and may install Node.js or the qhkit package locally.

Mitigation: Install only if the package and service are trusted; confirm installation and PATH changes before use.

Risk: The service needs an API token, and account lookups may consume paid Qinghu credits.

Mitigation: Confirm token setup, check the current credit estimate, and obtain user approval before paid calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shipinhao-account-info)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise natural-language answer with account details and credit usage; large results may be delivered as a file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a WeChat Channels finder username; check current pricing and request user approval before paid calls.]

## Skill Version(s):

0.1.2 (source: ClawHub server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
