## Description:

Generate AI videos, images, and audio with Runway API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slightly-unrelated](https://clawhub.ai/user/slightly-unrelated)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative engineers use this skill to generate video, image, and audio assets through Runway API calls from agent-authored JavaScript or shell examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, images, videos, or audio supplied to the skill may be sent to Runway's API.

Mitigation: Use only content that is approved for sharing with Runway and review Runway's API terms before use.

Risk: The skill requires a Runway API key stored in the environment.

Mitigation: Store RUNWAYML_API_SECRET in a managed secret store or local environment, avoid committing it, and rotate it if exposed.

Risk: Generation calls can consume Runway account credits.

Mitigation: Review model costs and account billing before running generated API calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/slightly-unrelated/skills/runwayml)
- [Runway API Documentation](https://docs.dev.runwayml.com/)
- [Runway Model Guide](https://docs.dev.runwayml.com/guides/models/)
- [Runway Developer Portal](https://dev.runwayml.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Runway API request examples, model choices, prompt guidance, and task polling instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
