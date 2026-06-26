## Description: <br>
Analyze the sentiment and emotional tone of text using NLTK and VADER. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[numbpill3d](https://clawhub.ai/user/numbpill3d) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to score short-form or conversational text for positive, negative, neutral, and compound sentiment signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use may download NLTK's VADER lexicon and store it locally. <br>
Mitigation: Preinstall the VADER lexicon before deployment or avoid this skill in tightly controlled offline environments. <br>
Risk: Sentiment scores can miss context, sarcasm, or domain-specific meaning. <br>
Mitigation: Use the scores as a signal for review or routing, not as the sole basis for high-impact decisions. <br>


## Reference(s): <br>
- [Sentinel Mood on ClawHub](https://clawhub.ai/numbpill3d/sentinel-mood) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON] <br>
**Output Format:** [JSON object with positive, negative, neutral, and compound sentiment scores] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns an error JSON object when no input text is provided or analysis fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
