## Description: <br>
Detect and redact PII from text files, including credit cards, SSNs, emails, API keys, addresses, and other supported categories, with no external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentward-ai](https://clawhub.ai/user/agentward-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, security teams, and agents use this skill to create sanitized copies of local text files before reviewing or sharing content that may contain PII. It can also preview detected PII categories and produce JSON summaries without printing raw PII values to stdout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional entity-map sidecar can contain original PII values. <br>
Mitigation: Treat any *.entity-map.json file as highly sensitive; do not read or share it unless required, store it carefully, and delete it when no longer needed. <br>
Risk: Raw input files may contain sensitive PII. <br>
Mitigation: Use --output to create a sanitized copy, inspect only the sanitized output, and avoid displaying raw input content in agent context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentward-ai/sanitize) <br>
- [AgentWard Project Homepage](https://github.com/agentward-ai/agentward) <br>
- [Supported PII Categories](references/SUPPORTED_PII.md) <br>
- [AgentWard Website](https://agentward.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; sanitized text files or JSON summaries when the local script is executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview and JSON modes avoid printing raw PII values. When --output is used, the optional *.entity-map.json sidecar can contain original PII and should be protected or deleted when no longer needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, clawhub.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
