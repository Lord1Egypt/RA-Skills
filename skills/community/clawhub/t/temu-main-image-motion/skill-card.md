## Description:

Turn one Temu main image into one Temu main image video for the listing video slot: a template one-shot that keeps that photo as the first frame, adds one preset move such as a turntable or light sweep, and returns one main image clip. Use it for Temu listing video and product main image motion — one photo one clip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers use this skill to turn an existing Temu listing main image into a short product-motion clip, with a planned single movement and a delivered video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shared Beatra authorization includes music, speech, voice-management, and credit-spending permissions beyond this video task.

Mitigation: Review the requested permissions before connecting, and revoke the device authorization in the Beatra Console if it is no longer wanted.

Risk: The bundled helper does not enforce seller approval before submitting paid video requests.

Mitigation: Review the current price and get explicit approval before every paid request; do not assume the helper will block an unapproved submission.

Risk: A selected product image is uploaded to Beatra for video generation.

Mitigation: Upload only the intended image and confirm it is appropriate to send for processing.

Risk: Installation analytics are automatic.

Mitigation: Inform users that analytics are sent during installation and review the service privacy information before connecting.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/beatra-ai/skills/temu-main-image-motion)
- [Beatra MCP service](https://mcp.beatra.ai/mcp)
- [Temu main image motion workflow](artifact/references/workflow.md)
- [Installation and authentication](artifact/references/installation-and-auth.md)
- [Billing, errors, and recovery](artifact/references/billing-errors-and-recovery.md)
- [Updates and security](artifact/references/updates-and-security.md)

## Skill Output:

**Output Type(s):** [Video, Guidance, Markdown]

**Output Format:** [A short generated video clip with a text shot plan and delivery summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One clip per approved image; supported duration is 2–15 seconds.]

## Skill Version(s):

0.2.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
