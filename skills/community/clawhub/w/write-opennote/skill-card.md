## Description:

Write, update, and read OpenNote notes through the public API. Use when the user wants to publish notes, upload note images, manage labels, or look up previously written notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liam-duan](https://clawhub.ai/user/liam-duan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, update, read, label, and enrich OpenNote notes through the OpenNote public API from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores note previews and note history in local .opennote files.

Mitigation: Avoid using it for highly sensitive notes unless local history is disabled, limited, or cleared after use.

Risk: The required OpenNote token can grant account-level note access.

Mitigation: Use a least-scoped, expiring token and revoke it promptly if it is no longer needed or may be compromised.

Risk: Shell commands may interpolate note content or URL parameters.

Mitigation: Prefer serialized JSON payload construction and URL encoding before sending API requests.

## Reference(s):

- [OpenNote](https://opennote.cc)
- [OpenNote App Store Listing](https://apps.apple.com/app/opennote-notes-journal/id6450187057)
- [OpenNote API Base URL](https://api.opennote.cc/api/v1)
- [ClawHub Skill Page](https://clawhub.ai/liam-duan/skills/write-opennote)
- [ClawHub Publisher Profile](https://clawhub.ai/user/liam-duan)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payloads, shell commands, and plain-text confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local .opennote cache and note-history JSON files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
