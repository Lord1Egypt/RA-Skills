## Description: <br>
Tetra Scar Safety helps agents check commands, file writes, network requests, and project directories using built-in threat rules and incident memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aibenyclaude-coder](https://clawhub.ai/user/aibenyclaude-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to screen proposed shell commands, file operations, network requests, and project directories before execution. It can also record prior incidents as local scar memory so similar future actions are blocked or warned on without an LLM call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Directory audits may inspect files that contain secrets or other sensitive local data. <br>
Mitigation: Run audits only on directories intended for inspection and review any findings before sharing them. <br>
Risk: Incident records may contain real secrets or sensitive operational details and influence future allow/block decisions. <br>
Mitigation: Avoid recording real secrets in incident text and periodically review or protect safety_scars.jsonl. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aibenyclaude-coder/tetra-scar-safety) <br>
- [Publisher profile](https://clawhub.ai/user/aibenyclaude-coder) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, Python dictionaries, JSON Lines scar records, and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Zero external Python dependencies; stores scar memory in safety_scars.jsonl by default.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
