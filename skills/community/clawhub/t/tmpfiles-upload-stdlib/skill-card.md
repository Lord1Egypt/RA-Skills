## Description:

Upload a local file to tmpfiles.org using Python standard library only, then return a direct download link in strict JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donigwapo](https://clawhub.ai/user/donigwapo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow automation users use this skill to upload an explicitly provided local file from an OpenClaw workspace or container to tmpfiles.org and receive a temporary public download URL as strict JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads user-selected local files to a public temporary file host.

Mitigation: Use it only for files intended to be temporarily public, and avoid secrets, credentials, private IDs, contracts, financial records, and other sensitive documents unless the user deliberately accepts that exposure.

## Reference(s):

- [tmpfiles.org](https://tmpfiles.org)
- [tmpfiles.org upload API](https://tmpfiles.org/api/v1/upload)
- [ClawHub skill page](https://clawhub.ai/donigwapo/skills/tmpfiles-upload-stdlib)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Code, Guidance]

**Output Format:** [Strict JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an existing local file path; uploaded files become temporarily public.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
