## Description: <br>
Summarize one supported site's current snapshot records and highest-signal items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit one imported Canvas, Gradescope, Edstem, or MyUW snapshot and quickly understand counts, top records, and recent updates without mutating source systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The snapshot path may expose private academic or workspace records to the agent. <br>
Mitigation: Provide only the intended snapshot file, keep outputs access-controlled, and review summaries before sharing them. <br>
Risk: The skill depends on @campus-copilot SDK or MCP sidecars that are referenced but not bundled in the artifact. <br>
Mitigation: Verify trusted versions and permissions for those dependencies in the target environment before use. <br>
Risk: A snapshot can be stale and should not be treated as live site truth. <br>
Mitigation: Label results as snapshot-based and avoid claims about current live browser or service state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaojiou176/site-overview-audit) <br>
- [examples/workspace-snapshot.sample.json](examples/workspace-snapshot.sample.json) <br>
- [examples/mcp/codex.example.json](examples/mcp/codex.example.json) <br>
- [examples/mcp/claude-desktop.example.json](examples/mcp/claude-desktop.example.json) <br>
- [skills/site-mcp-consumer/SKILL.md](skills/site-mcp-consumer/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only, snapshot-grounded site overview with counts, top items, and recent updates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
