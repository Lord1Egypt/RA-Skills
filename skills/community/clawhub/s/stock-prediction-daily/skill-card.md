## Description:

Predicts next-day direction for selected A-share stocks using Tencent daily market data, XGBoost training, prediction and evaluation scripts, and a local Flask dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yejiming](https://clawhub.ai/user/yejiming)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to train, tune, run, evaluate, and inspect daily A-share direction predictions, with supporting sector and stock analysis reports displayed in a local dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches market data and writes cached data, model files, and result files under the skill directory.

Mitigation: Install and run it only in an environment where this data access and local file creation are acceptable.

Risk: Saved .pkl and .joblib model artifacts should be treated as trusted executable artifacts.

Mitigation: Retrain locally or verify the source of copied or downloaded model files before loading them.

Risk: The dashboard may start a localhost service on port 5000, and force-killing that port can stop an unrelated process.

Mitigation: Identify the process bound to port 5000 before stopping it, and confirm it belongs to this dashboard.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yejiming/skills/stock-prediction-daily)
- [Configuration Reference](references/config-reference.md)
- [Troubleshooting Guide](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands plus generated CSV, JSON, model, scaler, and report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch market data, cache data, write model and results files, and start a localhost dashboard on port 5000.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
