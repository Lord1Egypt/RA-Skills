## Description:

Helps an agent prepare Seedance 2.0 video-generation prompts, model choices, API JSON parameters, and curl, JavaScript, or Python call examples for EvoLink text-to-video, image-to-video, and reference-to-video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xk103295870-alt](https://clawhub.ai/user/xk103295870-alt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to turn video ideas and referenced media into structured Seedance 2.0 prompts and EvoLink API request examples. It supports text-to-video, image-to-video, and multimodal reference-to-video planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and referenced media URLs may be sent to EvoLink or Seedance services when generated API calls are used.

Mitigation: Confirm the user is comfortable sending the prompt and referenced media URLs to EvoLink or Seedance before using the generated API calls.

Risk: The generated examples require an API key for an external video-generation service.

Mitigation: Use a user-owned SEEDANCE_API_KEY and avoid embedding credentials directly in generated code or shared artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xk103295870-alt/skills/seedance2-video-gen)
- [Seedance 2.0 API documentation](https://seedance2api.app)
- [EvoLink API signup](https://evolink.ai/signup)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON request bodies and curl, JavaScript, or Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated requests may reference user-provided image, video, or audio URLs and require a user-supplied SEEDANCE_API_KEY.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
