## Description:

Template-driven RapidAPI client with auto-registered actions and a universal call entrypoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[web3aivc](https://clawhub.ai/user/web3aivc)

### License/Terms of Use:


## Use Case:

Developers and agent workflows use this skill to make repeatable RapidAPI calls from JSON templates, list registered actions, import endpoint definitions, and receive normalized JSON or error responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send the user's RapidAPI key to non-RapidAPI or caller-chosen hosts by default.

Mitigation: Disable non-RapidAPI hosts by default, allowlist approved hosts, remove arbitrary direct calls, and verify or remove bundled non-RapidAPI templates before use with valuable credentials.

Risk: Request data and credentials are sent to external services selected by templates or direct-call input.

Mitigation: Use only trusted templates and endpoints, avoid sensitive inputs unless data sharing is approved, and document external-service handling expectations for users.

Risk: A RapidAPI key may already have been exposed through untrusted direct-call input or unverified templates.

Mitigation: Rotate the RapidAPI key if the implementation has been used with untrusted inputs or unverified templates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/web3aivc/skills/rapidapi)
- [Template Schema Details](docs/template-schema.md)
- [README](README.md)

## Skill Output:

**Output Type(s):** [API Calls, Code, Shell commands, Configuration]

**Output Format:** [JSON response objects with JavaScript and shell usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns stable ok/status/data/error/meta fields for API results.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact/package.json lists 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
