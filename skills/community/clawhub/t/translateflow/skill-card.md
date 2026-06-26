## Description: <br>
TranslateFlow helps agents translate text, localize content, adapt tone, and batch translate strings through the TranslateFlow API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jbennett111](https://clawhub.ai/user/Jbennett111) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, localization teams, and agents use this skill to translate text, localize application or document content, adapt tone, and batch translate multiple strings through TranslateFlow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Translation text and optional signup email are sent to the external TranslateFlow service. <br>
Mitigation: Do not translate secrets or regulated data without approval, and install only when use of TranslateFlow/Voss Consulting Group is acceptable. <br>
Risk: Auto-signup can print a full API key into logs. <br>
Mitigation: Prefer a dedicated API key and avoid running auto-signup in shared or persistent logging environments. <br>


## Reference(s): <br>
- [TranslateFlow ClawHub release](https://clawhub.ai/Jbennett111/translateflow) <br>
- [TranslateFlow translate endpoint](https://anton.vosscg.com/v1/translate) <br>
- [TranslateFlow key endpoint](https://anton.vosscg.com/v1/keys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include translated text returned by the TranslateFlow API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
