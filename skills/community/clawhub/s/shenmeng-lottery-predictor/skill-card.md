## Description: <br>
Analyzes Chinese sports and welfare lottery data, generates statistical number recommendations, and records prediction history for model-weight tuning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to run command-line or Python-based lottery analysis for supported Chinese lottery formats, including hot/cold number statistics, missing-value analysis, trend summaries, and recommendation reports. The artifact states that results are for entertainment and learning data analysis only and are not betting advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes an under-disclosed payment module that contacts SkillPay and contains a hardcoded API key. <br>
Mitigation: Review or remove payment.py before installation, rotate/remove the embedded key, and require clear documentation before enabling any payment verification behavior. <br>
Risk: Lottery recommendation output may be mistaken for reliable betting advice. <br>
Mitigation: Use results only for entertainment or learning-oriented data analysis and preserve the artifact's disclaimer that lottery outcomes are random and not predictable from history. <br>
Risk: The evolution feature records predictions and updates local JSON state. <br>
Mitigation: Inspect data/evolution_config.json and data/prediction_history.json before use and avoid storing sensitive user information in prediction records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenmeng/shenmeng-lottery-predictor) <br>
- [Publisher profile](https://clawhub.ai/user/shenmeng) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python snippets, shell commands, text reports, and JSON-backed local state files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and update local JSON files under data/ for evolution configuration and prediction history.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence, target metadata, artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
