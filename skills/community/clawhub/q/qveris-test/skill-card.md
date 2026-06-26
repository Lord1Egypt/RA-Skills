## Description: <br>
QVeris helps agents discover API tools by capability and call selected tools for structured data or external capabilities using a QVERIS_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linfangw](https://clawhub.ai/user/linfangw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to find API tools by capability, inspect candidates, and call a selected QVeris tool for structured data, media, extraction, translation, OCR, TTS, or similar external capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requests to QVeris and may invoke downstream external tools. <br>
Mitigation: Install only when QVeris and relevant downstream providers are approved for the intended data; avoid confidential inputs unless that approval exists. <br>
Risk: The QVERIS_API_KEY can authorize external tool discovery and execution. <br>
Mitigation: Use a dedicated API key, store it in the environment, and monitor usage or billing. <br>
Risk: Discovery finds API tools by capability, not factual answers, so poor queries or parameters can select the wrong tool or produce misleading results. <br>
Mitigation: Use English capability descriptions, inspect candidate parameters, validate returned data, and fall back to web search for factual or qualitative questions. <br>


## Reference(s): <br>
- [QVeris](https://qveris.ai) <br>
- [ClawHub skill page](https://clawhub.ai/linfangw/qveris-test) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API responses and shell commands when script execution is available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QVERIS_API_KEY; QVeris calls external APIs and large results may be returned as truncated content with a full-content URL.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
