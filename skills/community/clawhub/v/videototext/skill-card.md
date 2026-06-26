## Description: <br>
VideoToText guides agents through stable Bilibili official subtitle extraction, cookie and subtitle-track troubleshooting, and Chinese summary generation through an OpenAI-compatible chat-completions service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[willguo715](https://clawhub.ai/user/willguo715) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to parse Bilibili links, retrieve official subtitle text, troubleshoot login-visible subtitle tracks, and produce Chinese summaries from subtitle content. It is intended for use with the user's own Bilibili cookies and configured model provider credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bilibili session cookies are sensitive account credentials. <br>
Mitigation: Use only cookies from the user's own account, keep the .env file private, avoid shared or high-value accounts, and rotate cookies if exposed. <br>
Risk: When LLM summaries are enabled, subtitle text is sent to the configured OpenAI-compatible model provider. <br>
Mitigation: Enable summaries only with an approved provider and API key, and review subtitle content for sensitive information before sending it to the model endpoint. <br>
Risk: Aggressive Bilibili requests can trigger rate limits or access failures. <br>
Mitigation: Keep the built-in throttle, retry, and backoff settings enabled, and increase BILIBILI_MIN_INTERVAL_SECONDS if 412 or 429 responses occur. <br>
Risk: AI or login-visible subtitle tracks can be incomplete, unrelated, or unavailable without full cookies. <br>
Mitigation: Use the documented subtitle validation settings, provide complete Bilibili cookie fields when needed, and allow explicit language selection for known tracks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/willguo715/videototext) <br>
- [videototext reference](artifact/reference.md) <br>
- [Packaged source README](artifact/code/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, Python source modules, shell commands, environment-variable configuration, subtitle text, and Chinese summary text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [LLM summary input is capped at about 60000 characters; summary target length is clamped between 50 and 8000 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
