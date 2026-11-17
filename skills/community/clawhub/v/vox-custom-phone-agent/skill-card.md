## Description:

Converts natural-language phone tasks into TeddyMobile Vox custom bot outbound calls with guided missing-field collection, voice selection, safety checks, and trial or formal-account execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziliangzhu](https://clawhub.ai/user/ziliangzhu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a natural-language outbound calling goal into a structured Vox custom phone-agent request. It is suited for guided trial calls, formal Vox account integrations, and hosted deployments that keep Vox credentials outside the public skill package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real outbound phone calls.

Mitigation: Require explicit user confirmation before any call is started and enforce per-user call quotas.

Risk: Hosted API use can expose call initiation capability if left unauthenticated.

Mitigation: Require authentication for hosted endpoints and keep Vox credentials only on a controlled backend.

Risk: Call data, transcripts, analytics, or callbacks may expose sensitive information.

Mitigation: Minimize analytics, mask phone numbers, avoid returning full transcripts by default, and restrict callback destinations.

Risk: Callees may not understand that the caller is an AI voice assistant.

Mitigation: Disclose AI identity at call start and answer truthfully if the callee asks whether the caller is AI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ziliangzhu/skills/vox-custom-phone-agent)
- [SKILL.md](artifact/SKILL.md)
- [Get Started](artifact/GET_STARTED.md)
- [First Setup](artifact/FIRST_SETUP.md)
- [Registration Guide](artifact/REGISTRATION_GUIDE.md)
- [WorkBuddy Result Display Notes](artifact/WORKBUDDY.md)
- [Vox trial registration](https://vox-ai.teddymobile.cn/trial/apply)

## Skill Output:

**Output Type(s):** [text, markdown, json, api calls, configuration, guidance]

**Output Format:** [Markdown or JSON-like structured results with follow-up questions, masked phone numbers, Vox request status, requestId, task summaries, and registration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate outbound Vox API calls when required fields are complete and safety checks pass; trial mode uses the credential-free Vox trial endpoint, while formal mode requires Vox credentials.]

## Skill Version(s):

1.0.6 (source: ClawHub server release evidence; artifact manifests report 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
