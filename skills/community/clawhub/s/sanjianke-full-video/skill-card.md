## Description:

Helps agents submit and check text-to-video, first-and-last-frame, and reference-media video generation tasks through the a7w API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Creators and developers use this skill to configure an a7w API key, submit video-generation jobs, and retrieve task status and results. The included client also exposes other a7w plugins available to that key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included client can inspect and call a7w plugins beyond the video endpoints described in the skill overview.

Mitigation: Use a limited API key where possible and review the requested plugin and operation before running a command.

Risk: Changing the API host can send the user's API key to an untrusted destination.

Mitigation: Do not set --host or A7W_HOST unless the destination is trusted.

Risk: Repeated video task submissions may consume account credits.

Mitigation: Check the existing task's status before resubmitting, and confirm applicable charges in the a7w account.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/2253128/skills/sanjianke-full-video)
- [a7w API and account setup](https://api.a7w.cn/)
- [Getting started](references/getting-started.md)
- [Video task submission reference](references/api-submit.md)
- [Video task query reference](references/api-query.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Guidance]

**Output Format:** [Markdown instructions and JSON task responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided a7w API key; video generation returns task identifiers to check for results.]

## Skill Version(s):

1.0.7 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
