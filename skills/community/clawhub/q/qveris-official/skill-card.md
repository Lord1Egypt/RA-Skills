## Description: <br>
QVeris helps agents discover specialized API tools by capability and call selected tools for structured data, media, document, translation, OCR, TTS, and related workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linfangw](https://clawhub.ai/user/linfangw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to find API tools by capability, inspect tool metadata, and call the selected tool through QVeris when local or native tools do not cover the request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses QVERIS_API_KEY to access an external tool gateway. <br>
Mitigation: Protect the API key and avoid sending secrets or private documents unless QVeris and the selected tool are trusted. <br>
Risk: Selected external tools may perform sensitive, costly, or account-changing actions. <br>
Mitigation: Review sensitive, costly, or account-changing calls before allowing execution. <br>


## Reference(s): <br>
- [QVeris homepage](https://qveris.ai) <br>
- [QVeris API base URL](https://qveris.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool calls require QVERIS_API_KEY and may return truncated large results with a full-content URL.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
