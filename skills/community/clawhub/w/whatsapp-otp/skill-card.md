## Description:

Send WhatsApp OTP (one-time password) messages via CMI OmniChannel RCS API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[picccabo-art](https://clawhub.ai/user/picccabo-art)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to send verification, OTP, or authentication codes over WhatsApp through a pre-configured CMI OmniChannel RCS template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API secrets and OTPs are sent by an implementation that disables important network security protections.

Mitigation: Use only in approved environments with direct access to the CMI endpoint, fix certificate validation and proxy handling before real OTP use, and rotate any credentials already used with this implementation.

Risk: Credentials may be exposed when passed as command-line arguments.

Mitigation: Prefer environment variables, a secret manager, or another non-logged secret delivery path instead of passing credentials directly on the command line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/picccabo-art/skills/whatsapp-otp)
- [CMI OmniChannel RCS singleSend endpoint](https://cpaas-rcs.cmidict.com:7081/singleSend)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown with inline shell commands and command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CMI tenant credentials, application credentials, recipient phone number, and OTP code.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
