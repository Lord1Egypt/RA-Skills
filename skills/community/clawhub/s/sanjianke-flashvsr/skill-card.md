## Description:

Helps agents submit video super-resolution jobs to the a7w flashvsr service and check their results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Creators and developers use this skill to submit videos for super-resolution processing and retrieve task status and results through their own a7w account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled client can call a7w marketplace APIs beyond video super-resolution using the user's API key.

Mitigation: Review before installing and run only commands explicitly targeting flashvsr.

Risk: Private or tokenized input video URLs may be disclosed to the third-party processing service.

Mitigation: Submit only video URLs approved for third-party processing.

Risk: A custom host can receive the user's API key.

Mitigation: Do not set --host or A7W_HOST to an untrusted server.

Risk: Repeated job submissions can incur additional charges.

Mitigation: Check task status before resubmitting a job.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/2253128/skills/sanjianke-flashvsr)
- [Getting started with a7w](artifact/references/getting-started.md)
- [Submit API](artifact/references/api-submit.md)
- [Query API](artifact/references/api-query.md)
- [a7w API platform](https://api.a7w.cn/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON]

**Output Format:** [Text instructions and JSON task responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task ID and status; a processed video URL when available. API calls require a user-provided key and may incur charges.]

## Skill Version(s):

1.0.7 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
