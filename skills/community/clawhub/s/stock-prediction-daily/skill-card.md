## Description: <br>
Trains and runs an XGBoost-based A-share daily price-direction prediction workflow using Tencent daily market data, CSV and JSON reports, evaluation, and a local Flask dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yejiming](https://clawhub.ai/user/yejiming) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to train, tune, run, and evaluate A-share daily direction predictions and to view generated reports in a local dashboard. The skill is suited for workflow automation and market-analysis support, with results reviewed before operational or investment use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public market-data fetching and model-generated stock predictions can be stale, unavailable, or inaccurate. <br>
Mitigation: Evaluate predictions against subsequent trading data, review generated reports, and avoid treating the output as standalone financial advice. <br>
Risk: The workflow creates local cache, model, result, prediction-history, and report files. <br>
Mitigation: Run it from the documented skill scripts directory and review generated files before reusing, publishing, or deleting them. <br>
Risk: The troubleshooting guide documents a forceful kill command for port 5000. <br>
Mitigation: Verify the process using port 5000 and prefer a graceful stop before using kill -9. <br>
Risk: Sector and watchlist analysis depend on named companion skills. <br>
Mitigation: Install and review those companion skills before relying on sector or stock-analysis outputs. <br>


## Reference(s): <br>
- [Configuration Reference](references/config-reference.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, plus generated CSV, JSON, pickle, and Markdown report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local data, model, result, prediction-history, and report directories under the skill scripts directory; the Flask dashboard is served on 127.0.0.1:5000.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
