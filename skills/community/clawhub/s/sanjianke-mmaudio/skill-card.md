## Description:

Helps agents submit video sound-effect and dubbing requests to the a7w mmaudio service and check task results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2253128](https://clawhub.ai/user/2253128)

### License/Terms of Use:

MIT

## Use Case:

Creators and developers use this skill to generate audio for video through a7w, submit asynchronous jobs, and retrieve their results using their own API key and paid account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated requests can be redirected to a host other than a7w.cn.

Mitigation: Do not override the service host unless you explicitly trust the destination; review saved configuration after login.

Risk: Media URLs, prompts, task data, and API credentials are shared with the service.

Mitigation: Use only media and account data you are comfortable sharing with a7w.cn; avoid private or sensitive signed URLs without checking its retention and access policies.

Risk: Repeated task submissions can consume additional paid credits.

Mitigation: Check an existing task ID before resubmitting, and monitor account usage.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/2253128/skills/sanjianke-mmaudio)
- [Getting started and API key setup](artifact/references/getting-started.md)
- [Submit task API](artifact/references/api-submit.md)
- [Query task API](artifact/references/api-query.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance and JSON task responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task IDs and status or result data; service calls require a personal API key and may incur charges.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata; bundled frontmatter says 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
