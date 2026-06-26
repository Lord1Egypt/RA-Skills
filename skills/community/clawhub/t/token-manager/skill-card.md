## Description: <br>
Universal LLM Token Manager - Monitor usage and provide cost-saving recommendations for Kimi, OpenAI, Anthropic, Gemini, and local models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kelegele](https://clawhub.ai/user/kelegele) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to monitor LLM token usage, estimate costs, check supported provider balances, set up balance alerts, and review cross-session spending patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can accept API keys as command-line arguments while its documentation says keys are read only from environment variables. <br>
Mitigation: Prefer environment variables for API keys and avoid passing secrets as command arguments. <br>
Risk: Provider token-estimation APIs may receive prompt text when estimation is enabled. <br>
Mitigation: Avoid sending sensitive prompt text through provider token-estimation APIs. <br>
Risk: Recurring balance checks may continue after the user no longer wants monitoring. <br>
Mitigation: Remove any cron job when recurring balance checks are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page for Token Manager](https://clawhub.ai/kelegele/token-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON report output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local usage, balance, alert, and session analytics outputs; scheduled checks can persist local alert state.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
