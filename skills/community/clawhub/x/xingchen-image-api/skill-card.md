## Description:

Helps agents submit Xingchen AI image-generation requests and monitor results using a customer-owned API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moyudawang520](https://clawhub.ai/user/moyudawang520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ecommerce teams use this skill to generate or edit product images through Xingchen AI and check job status before sharing previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts, job IDs, and reference image URLs are sent to the configured Xingchen AI endpoint.

Mitigation: Use a trusted Xingchen domain and send only content you intend to share with that service.

Risk: A disclosed customer API key is used to submit and monitor image jobs.

Mitigation: Keep XINGCHEN_API_KEY in the environment rather than chat or logs.

## Reference(s):

- [Xingchen AI customer image API reference](references/api.md)
- [Xingchen Image API on ClawHub](https://clawhub.ai/moyudawang520/skills/xingchen-image-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with image preview links and task status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include job IDs, preview URLs, and safe error messages.]

## Skill Version(s):

1.0.0 (source: server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
