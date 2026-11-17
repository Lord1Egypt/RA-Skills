## Description:

Paid video generation skill for text-to-video and image-to-video, covering animation, short films, motion clips, and product demos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn text prompts or a single reference image into a paid WorkRally-generated video, animation, short clip, or product demo after payment authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each generation is a paid action through WeChat Pay.

Mitigation: Show the service name and 6.88 RMB price before invoking payment, and use the same payment_id for content polling so retries do not restart the payment flow.

Risk: Reference images are sent to WorkRally's cloud service for processing.

Mitigation: Do not use sensitive images unless that transfer is acceptable to the user.

Risk: Generated result links are documented as short-lived.

Mitigation: Present the link promptly and guide the agent to save or download the result when possible.

Risk: Video generation is asynchronous and may require polling before delivery.

Mitigation: Follow the documented status handling: wait and retry content on generating, do not re-invoke while a payment_id is active, and stop on terminal failed, expired, or refunded states.

## Reference(s):

- [WorkRally homepage](https://workrally.qq.com)
- [ClawHub skill page](https://clawhub.ai/tencent-adm/skills/workrally-video)
- [Prompting guide](references/prompting.md)
- [Invoke flow](references/invoke-flow.md)
- [Pricing](references/pricing.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text]

**Output Format:** [Markdown instructions with HTTP and JSON examples; runtime output is a generated video result URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WeChat Pay authorization; each request returns one cloud-generated 720p video, defaults to 10 seconds, and result links are documented as short-lived.]

## Skill Version(s):

1.1.1 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
