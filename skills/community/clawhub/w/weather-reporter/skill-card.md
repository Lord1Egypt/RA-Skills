## Description:

Weather Reporter generates a detailed weather report image for a requested city using wttr.in weather data, chart rendering, AI-generated background imagery, and short AI weather tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyt64](https://clawhub.ai/user/zyt64)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to generate a city-specific weather briefing image with charts, daily conditions, and concise weather tips. It is suited for automated report generation where external weather and AI services are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may delete or overwrite common image filenames in the current working directory.

Mitigation: Run it only in a dedicated folder or virtual environment and keep unrelated image files outside that directory.

Risk: The skill uses external weather and AI services, so city names, weather data, prompts, and generated image requests may be sent to configured providers.

Mitigation: Review provider settings before use and avoid submitting sensitive locations or confidential context.

Risk: config.json stores API credentials needed for the AI services.

Mitigation: Treat config.json as sensitive, avoid committing it, and rotate credentials if they are exposed.

## Reference(s):

- [ClawHub Weather Reporter release page](https://clawhub.ai/zyt64/skills/weather-reporter)
- [wttr.in weather data service](https://wttr.in/)
- [Zhipu AI platform](https://open.bigmodel.cn/)

## Skill Output:

**Output Type(s):** [files, text, configuration, shell commands, guidance]

**Output Format:** [PNG image file with console status text and configuration-driven API usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates output.png and temporary image files in the working directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
