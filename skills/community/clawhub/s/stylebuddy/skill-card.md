## Description:

StyleBuddy is a Chinese-language wardrobe assistant that helps users record clothing items, manage a local wardrobe, recommend outfits, evaluate shopping candidates, and generate wardrobe analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[89kpjddmtb-ui](https://clawhub.ai/user/89kpjddmtb-ui)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users can use StyleBuddy as a wardrobe and outfit assistant for clothing intake, outfit recommendations, shopping comparisons, wardrobe summaries, and local backup or restore workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores clothing photos, wardrobe records, preferences, wishlist data, and backups locally.

Mitigation: Install only when local storage of this personal wardrobe data is acceptable, and review where image, database, and backup files are written before use.

Risk: The advertised automatic image recognition is stronger than the implemented placeholder and fallback behavior.

Mitigation: Treat image-derived clothing details as unverified unless the publisher adds a real recognition implementation and clear privacy controls.

Risk: Broad trigger phrases may activate the assistant in ordinary clothing or shopping conversations.

Mitigation: Review and narrow the configured triggers before deployment if unintended activation would expose personal clothing or preference data.

## Reference(s):

- [ClawHub StyleBuddy release page](https://clawhub.ai/89kpjddmtb-ui/skills/stylebuddy)
- [StyleBuddy feature design document](https://feishu.cn/docx/KRdZdGqScopSdUxF7rHcAUyPn2f)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, images]

**Output Format:** [Markdown-like Chinese text responses, optional image path lists, and local JSON backup data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from local wardrobe records, bundled outfit templates, optional weather data, and saved local image files.]

## Skill Version(s):

0.4.4 (source: server release metadata and agent.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
