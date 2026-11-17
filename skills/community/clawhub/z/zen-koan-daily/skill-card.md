## Description:

Daily Zen Buddhist koan lecture with Chinese ink wash illustration and TTS audio, producing classical text, background, interpretation, modern insight, image guidance, and narration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yumyumtum](https://clawhub.ai/user/yumyumtum)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate daily Zen koan study material, including bilingual lecture text, contemplative image prompts or images, and TTS narration for personal practice or content creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the documented image workflow asks the agent to run a generated shell command targeting an undeclared external yumfu script with shell-formatted dynamic arguments.

Mitigation: Review the generated image command before execution, verify the external dependency is installed and trusted, and avoid automatically executing image commands until dynamic arguments are safely handled.

Risk: Lecture text, prompts, or personalized context may be sent to optional web search, Google Gemini, or Edge TTS services.

Mitigation: Do not include sensitive personal context in prompts or narration text, and disable optional web search or external media generation when privacy requirements do not allow third-party service use.

## Reference(s):

- [Zen Koan Daily ClawHub page](https://clawhub.ai/yumyumtum/skills/zen-koan-daily)
- [Publisher profile](https://clawhub.ai/user/yumyumtum)
- [Artifact homepage](https://github.com/yumyumtum/YumSkills/tree/main/zen-koan-daily)
- [Koan reference data](references/koans.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown lecture text with optional JSON metadata, shell commands, PNG image output, and MP3 audio output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use optional web search, Google Gemini image generation, and Edge TTS; generated media is written to a local outbound media directory.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
