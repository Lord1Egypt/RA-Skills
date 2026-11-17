## Description:

Verimor API uzerinden SMS gonder, bakiye sorgula, rapor al, basliklari listele ve kara liste yonet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirzakarahan-verimor](https://clawhub.ai/user/mirzakarahan-verimor)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and business operators use this skill to let an agent send Verimor SMS messages, check SMS credit balance, inspect delivery status, list sender headers, cancel scheduled campaigns, and manage blacklist entries.

### Deployment Geography for Use:

Global, with workflows documented for Turkish-format phone numbers.

## Known Risks and Mitigations:

Risk: The skill gives an agent direct authority to send paid SMS messages and change campaign or blacklist state.

Mitigation: Require explicit operator confirmation before every send, campaign cancellation, and blacklist change.

Risk: Several documented commands place account credentials in URL query strings, which may expose them in logs or shared environments.

Mitigation: Prefer safer credential handling if Verimor supports it, and rotate credentials if URL-based commands may already have been logged.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirzakarahan-verimor/skills/verimor-sms)
- [Verimor SMS API endpoint](https://sms.verimor.com.tr/v2)

## Skill Output:

**Output Type(s):** [Text, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown with bash curl and jq command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, VERIMOR_USERNAME, VERIMOR_PASSWORD, and VERIMOR_SOURCE.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
