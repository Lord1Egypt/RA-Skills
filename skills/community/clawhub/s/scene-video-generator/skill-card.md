## Description:

Generates short AI scene video clips from storyboard or scene descriptions using configurable providers including Jimeng, Kling, Runway, Pika, and Vidu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oliviapp8](https://clawhub.ai/user/oliviapp8)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, developers, and production teams use this skill to turn storyboard scene descriptions or reference images into short AI-generated scene clips. It is suited for non-avatar scenes such as environments, product shots, background action, and storyboard batches that feed a video stitching workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference images may be sent to the configured external video provider.

Mitigation: Avoid private, regulated, or copyrighted material unless sharing it with that provider is acceptable.

Risk: Provider API credentials may be exposed if stored in source control or shared configuration.

Mitigation: Store API keys outside source control, restrict access to credential-bearing config files, and rotate keys if exposed.

Risk: Complex motion, multi-person scenes, and provider-specific prompt limits can produce unstable or inconsistent results.

Mitigation: Run small test batches first, keep prompts within provider limits, and save seeds for reproducible satisfactory outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oliviapp8/skills/scene-video-generator)
- [Backend setup guide](references/backend-setup.md)
- [Prompt optimization guide](references/prompt-guide.md)
- [Jimeng documentation](https://www.volcengine.com/docs/jimeng/)
- [Runway documentation](https://docs.runwayml.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with YAML-style video metadata and provider URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include video id, backend, URL, duration, resolution, aspect ratio, prompt, seed, and completion status.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
