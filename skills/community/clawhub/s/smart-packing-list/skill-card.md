## Description:

根据目的地实时天气、行程天数、出行类型和旅行者构成，智能生成个性化打包清单，支持打包进度检查和出行贴士提醒。

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers use this skill to generate weather-aware packing lists, quick packing lists, travel tips, and progress checks for packed items before a trip.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather-enabled generation sends trip destinations to an external proxy while the artifact also states that no external requests occur.

Mitigation: Correct the privacy and data-flow description before deployment, document the proxy operator and retention expectations, and use quick mode when destinations are sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/smart-packing-list)
- [Publisher profile](https://clawhub.ai/user/travel-skills)
- [Gaode weather proxy used by weather-enabled mode](https://gaode-proxy-jerspxcked.cn-hangzhou.fcapp.run)

## Skill Output:

**Output Type(s):** [JSON, guidance]

**Output Format:** [JSON objects containing weather summaries, categorized packing lists, essential/optional markers, progress checks, alerts, and travel tips.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generate mode uses destination weather data; quick and check modes use local checklist logic.]

## Skill Version(s):

1.0.19 (source: server release metadata; artifact frontmatter says 1.0.3 and artifact _meta.json says 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
