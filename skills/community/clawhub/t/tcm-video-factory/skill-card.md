## Description:

Automate health video production planning (Topic Research - Script - Character - Image/Video Prompts) using Perplexity API. Based on TCM Video Factory workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xaotiensinh-abm](https://clawhub.ai/user/xaotiensinh-abm)

### License/Terms of Use:


## Use Case:

Content creators, developers, and production teams use this skill to turn a health topic into a video production plan with topic research, a character prompt, a four-part script, image prompts, and VEO3 video prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The requested topic and generated planning context are sent to Perplexity using the user's API key.

Mitigation: Avoid private health details, proprietary campaign information, and regulated personal data unless the use fits the user's Perplexity data-handling requirements.

Risk: Generated health video scripts and prompts may include claims that need domain review before publication.

Mitigation: Review generated plans for accuracy, appropriate disclaimers, and Vietnamese-language production fit before using them in public content.

## Reference(s):

- [TCM Video Factory on ClawHub](https://clawhub.ai/xaotiensinh-abm/skills/tcm-video-factory)
- [Publisher profile: xaotiensinh-abm](https://clawhub.ai/user/xaotiensinh-abm)
- [Perplexity Chat Completions API endpoint](https://api.perplexity.ai/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown file with production-plan sections and inline prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a timestamped PLAN_[Timestamp].md file in the current working directory.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
