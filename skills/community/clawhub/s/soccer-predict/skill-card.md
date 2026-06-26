## Description: <br>
Football match betting prediction system that collects pre-match data from titan007.com, runs a five-step quantitative analysis framework, and outputs betting recommendations with predicted scores. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superluigi0309](https://clawhub.ai/user/superluigi0309) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect football match data, calculate probabilities and expected value for Asian handicap and over/under markets, and produce concise or visual betting analysis. It can also review completed matches, adjust model weights, and report accumulated prediction accuracy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may save football prediction history and learned model changes in local memory files without clear opt-in or cleanup controls. <br>
Mitigation: Require explicit user confirmation before post-match review writes memory, and document how to review or remove saved football prediction memory files. <br>
Risk: The skill browses titan007.com for match data during prediction workflows. <br>
Mitigation: Use it only when browsing that data source is acceptable, and review collected match data before relying on the analysis. <br>
Risk: The skill outputs betting analysis and recommendations that may be wrong or misleading. <br>
Mitigation: Present outputs as uncertain analysis, not financial or gambling advice, and require human review before any betting-related decision. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/superluigi0309/soccer-predict) <br>
- [Data Collection Guide](references/data-collection.md) <br>
- [Prediction Framework](references/prediction-framework.md) <br>
- [Post-Match Review & Learning Framework](references/review-framework.md) <br>
- [Titan007 Data Source](https://zq.titan007.com/) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, HTML, Guidance, Configuration] <br>
**Output Format:** [Markdown or HTML reports with probability tables, expected-value calculations, betting recommendations, predicted scores, and post-match review notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local memory files during post-match review to persist prediction history and learned weights.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact CHANGELOG.md and clawhub.json list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
