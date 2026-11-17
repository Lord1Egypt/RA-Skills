## Description:

Helps agents use the Vizard.ai API to clip long videos into social-ready shorts, edit short videos with subtitles or B-roll, publish clips to social platforms, and generate AI captions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vizardai](https://clawhub.ai/user/vizardai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to automate Vizard.ai video workflows, including clip generation, short-form edits, caption generation, and approved social publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The publishing workflow can post to a connected social account without an explicit confirmation step in the example.

Mitigation: Require the agent to show the exact clip, destination platform and account, caption, and schedule, then obtain explicit user approval before calling the publish endpoint.

## Reference(s):

- [Vizard API full reference](api-reference.md)
- [Supported languages](https://docs.vizard.ai/docs/supported-languages)
- [Rate limits](https://docs.vizard.ai/docs/rate-limit)
- [Pricing](https://docs.vizard.ai/docs/pricing)
- [ClawHub skill page](https://clawhub.ai/vizardai/skills/vizard-api-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with REST endpoint guidance, JSON request examples, and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Vizard.ai API key and a paid Vizard plan; generated video URLs expire after 7 days.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
