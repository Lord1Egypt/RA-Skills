## Description:

Give your agent the ability to instantly take screenshots of any website with just the URL. Cloud-based so your agent has to perform no work. Free forever, open source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kav-k](https://clawhub.ai/user/kav-k)

### License/Terms of Use:


## Use Case:

Developers and automation builders use this skill to register for a cloud screenshot API and capture public or intentionally shareable web pages as PNG or JPEG files from a URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive cookies, headers, API keys, internal URLs, or private pages could be sent to a third-party screenshot service.

Mitigation: Use the service only for public or intentionally shareable URLs unless the provider is explicitly trusted, and avoid sending credentials or private pages unless credentials are short-lived, narrowly scoped, and safe to expose.

Risk: The service API key cannot be recovered after registration.

Mitigation: Store the API key securely when it is issued and rotate by registering an appropriate replacement if it is lost or exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kav-k/skills/snap)
- [Publisher profile](https://clawhub.ai/user/kav-k)
- [Snap screenshot service](https://snap.llm.kaveenk.com)
- [API registration endpoint](https://snap.llm.kaveenk.com/api/register)
- [API screenshot endpoint](https://snap.llm.kaveenk.com/api/screenshot)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Files]

**Output Format:** [Markdown guidance with bash and Python examples; screenshot responses are PNG or JPEG binary files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a service API key. Documented limits include 2 screenshots per minute, 200 screenshots per day, 16384px maximum full-page height, and 10MB maximum screenshot size.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
