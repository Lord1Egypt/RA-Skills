## Description:

Use Chanjing customised person APIs to create, inspect, list, poll, and delete custom digital humans from uploaded source videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyuting214](https://clawhub.ai/user/zuoyuting214)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage Chanjing custom digital-human assets: upload source videos, create customised person tasks, inspect or list assets, poll build status, and delete assets when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload real-person source videos to the Chanjing service.

Mitigation: Only process videos when the user confirms they have the rights and consent to upload and transform the source material.

Risk: The skill relies on local Chanjing credentials and token caching.

Mitigation: Keep the credentials file protected, use the configured credential directory intentionally, and avoid exposing app_id, secret_key, or access tokens in shared logs.

Risk: The skill can delete custom digital-human assets from an account.

Mitigation: Require explicit confirmation with the exact person_id before running delete_person.

Risk: The security verdict recommends review before installation for real-person videos or production Chanjing assets.

Mitigation: Review the skill before deployment and confirm the operational workflow matches the intended production controls.

## Reference(s):

- [Chanjing Open API](https://open-api.chanjing.cc)
- [Skill reference](artifact/reference.md)
- [Usage examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or text API results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Chanjing identifiers, preview URLs, detail JSON, and credential setup guidance.]

## Skill Version(s):

0.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
