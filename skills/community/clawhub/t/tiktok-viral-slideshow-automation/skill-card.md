## Description:

Automates educational TikTok slideshow creation, AI image generation setup, AutomateClips uploads, scheduling guidance, and performance tracking for an app or product.

This skill is ready for commercial/non-commercial use.

## Publisher:

[julianriss](https://clawhub.ai/user/julianriss)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and growth teams use this skill to set up and run a repeatable TikTok slideshow workflow for promoting apps or products. It helps collect campaign inputs, generate slide plans and image prompts, upload finished slideshows through AutomateClips, and log performance for later iteration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend image-generation credits while producing slideshow assets.

Mitigation: Use dedicated API credentials, monitor provider usage, and set billing or rate limits before running recurring workflows.

Risk: The skill can publish TikTok content through AutomateClips, including on a recurring schedule.

Mitigation: Review generated slides, captions, and upload settings manually during dry runs before enabling any schedule.

Risk: The custom generation option can run user-pasted commands with limited guardrails.

Mitigation: Use a dedicated project directory, provide only minimal environment variables, and run custom commands only after reviewing and trusting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/julianriss/skills/tiktok-viral-slideshow-automation)
- [Publisher profile](https://clawhub.ai/user/julianriss)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON snippets, Python examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local project files, slideshow tracking JSON entries, image generation prompts, upload commands, and optional scheduling prompts.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
