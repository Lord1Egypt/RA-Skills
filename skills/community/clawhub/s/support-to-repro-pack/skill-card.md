## Description: <br>
Convert support tickets, logs, and screenshots into sanitized, reproducible engineering issue packs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mshs01156](https://clawhub.ai/user/mshs01156) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support engineers use this skill to convert messy customer support tickets, logs, screenshots, and related context into sanitized engineering handoff materials. It helps produce reproducible issue packs with extracted facts, timelines, severity assessment, follow-up questions, internal escalation notes, and a customer-safe reply. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive customer data may remain in generated outputs because the release security evidence says the sanitization promises are stronger than the artifacts support. <br>
Mitigation: Use only authorized inputs, inspect every generated file before sharing, avoid ZIP packaging until outputs are checked, and do not rely on automated redaction as complete protection for logs, screenshots, URLs, tokens, derived timelines, or stack-trace files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mshs01156/support-to-repro-pack) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown documents, JSON reports, sanitized text files, and optional ZIP archive] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an engineering issue, internal escalation summary, customer reply, facts report, timeline, redaction report, and sanitized ticket and log artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
