## Description:

Find trending topics, create editorial-style social media graphics, and post to X/Twitter and Instagram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashmonmc](https://clawhub.ai/user/ashmonmc)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to research viral topics, generate editorial social graphics, and prepare or publish posts on X/Twitter and Instagram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access social accounts and publish live content.

Mitigation: Use a dedicated Instagram account, review all generated captions and commands before posting, and confirm each target channel before execution.

Risk: Credentials and API keys are required for Instagram, Brave Search, OpenAI image generation, and X/Twitter tooling.

Mitigation: Prefer environment variables or managed configuration, avoid passing passwords on the command line, and rotate credentials after testing.

Risk: Untrusted search queries or captions may be unsafe while shell or code injection issues remain unresolved.

Mitigation: Treat external text as untrusted, inspect generated commands before running them, and avoid using unsanitized user input in posting or search workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ashmonmc/skills/viral-content-engine)
- [OpenAI Images API endpoint used by artifact](https://api.openai.com/v1/images/generations)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with command examples, terminal result text, generated image files, and social post result links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authenticated third-party tools and API keys for search, image generation, and posting.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
