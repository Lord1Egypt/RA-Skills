## Description: <br>
Audit an OpenClaw agent's memory for staleness, redundancy, dark records, and contradictions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rudi193-cmd](https://clawhub.ai/user/rudi193-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect OpenClaw memory files, identify stale, redundant, dark, or contradictory records, and choose cleanup actions with confirmation before changes are made. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect markdown files in the memory directory selected by the user. <br>
Mitigation: Review the target directory and exact files before running the diagnostic. <br>
Risk: Cleanup recommendations may involve archiving, merging, qmd re-indexing, or appending a memory summary. <br>
Mitigation: Confirm each file move, merge, index update, or append-only memory write before making changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rudi193-cmd/willow-memory-health) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with optional JSON diagnostic output and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect markdown files in a user-selected memory directory; cleanup actions should be confirmed before moving, merging, re-indexing, or appending summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
