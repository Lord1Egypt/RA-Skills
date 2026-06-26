## Description: <br>
Replace base64 images in session history with context-aware text descriptions, reducing image token cost by 96-99%. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joelovestech](https://clawhub.ai/user/joelovestech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to reduce multimodal context size in OpenClaw sessions by replacing stored image blocks with text descriptions. It is intended for sessions approaching context limits or workflows that need token-cost optimization across one or more agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session images and nearby conversation context are sent to Anthropic for description generation. <br>
Mitigation: Install only when that disclosure is acceptable; prefer explicit ANTHROPIC_API_KEY configuration, run dry-run first, and use --redact for sensitive sessions. <br>
Risk: Live runs modify local OpenClaw session JSONL files. <br>
Mitigation: Keep backups enabled, review dry-run output before live execution, and avoid --no-backup unless external recovery is already in place. <br>
Risk: Redaction changes what is saved in generated descriptions but does not make the original image local-only. <br>
Mitigation: Use --redact to reduce persisted sensitive text, and treat the original image plus surrounding context as data sent to the Anthropic API. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/joelovestech/shrink) <br>
- [Anthropic Messages API endpoint](https://api.anthropic.com/v1/messages) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live runs can rewrite OpenClaw session JSONL files and create .bak backups; dry-run and JSON modes are available for review before changes.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
