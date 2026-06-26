## Description: <br>
Estimates request token usage and supports token counting across multiple model families. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[largetool](https://clawhub.ai/user/largetool) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to estimate input, output, and total token usage before sending prompts. It can provide model-aware counts, JSON output, usage-meter display, and compression-savings guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tokenizer dependencies or assets may be missing or uncached, which can cause downloads or fallback estimates. <br>
Mitigation: Install and pin required dependencies in a controlled environment, pre-cache tokenizer assets, or block network access when offline operation is required. <br>
Risk: Token estimates can be inaccurate, especially when fallback character counting is used for short text. <br>
Mitigation: Treat results as planning guidance and confirm actual usage with provider billing or API usage data for cost-sensitive workflows. <br>
Risk: Broad triggers may invoke the skill in unintended contexts. <br>
Mitigation: Invoke it with explicit commands such as /token or a direct script command when estimating sensitive or cost-sensitive text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/largetool/token-estimator) <br>
- [Publisher profile](https://clawhub.ai/user/largetool) <br>
- [Test report](tests/test-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [Human-readable text report or JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Estimates are approximate; tokenizer dependencies may download or require cached assets, and fallback character counting is less accurate for short text.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
