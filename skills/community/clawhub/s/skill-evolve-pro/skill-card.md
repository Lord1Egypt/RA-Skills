## Description: <br>
Skill Evolve Pro helps agents improve skill documents by analyzing failed trajectories or SESSION-STATE data, generating edit patches, and verifying updates through a ReflACT-style loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pengpengliu1212-art](https://clawhub.ai/user/pengpengliu1212-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to analyze failed skill executions, propose bounded SKILL.md edits, and maintain longer-term guidance for target skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local skill files, failure traces, and SESSION-STATE-derived data may be processed by DeepSeek. <br>
Mitigation: Use only in workspaces where that data may be shared with DeepSeek, and remove sensitive content from traces before running the skill. <br>
Risk: The skill can persistently rewrite target skill documents. <br>
Mitigation: Keep backups of target skills and require a manual diff review before allowing any SKILL.md write. <br>
Risk: The artifact includes an exposed bundled API key. <br>
Mitigation: Remove the bundled key and configure a trusted DeepSeek endpoint and API key through private environment variables or local configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/pengpengliu1212-art/skill-evolve-pro) <br>
- [Publisher profile](https://clawhub.ai/user/pengpengliu1212-art) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with JSON-like patch data and optional edited skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DeepSeek API credentials; may modify target skill documents after user confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
