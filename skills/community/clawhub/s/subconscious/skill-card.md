## Description: <br>
A bounded, governed self-improvement layer for OpenClaw agents that consumes learnings, evolves them through typed mutations, and surfaces active behavioral patterns as session biases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elyasdruid](https://clawhub.ai/user/elyasdruid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to maintain a bounded local memory layer that turns self-improvement learnings into governed session biases for future agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring background jobs can change local memory state and influence future agent behavior without a user being present. <br>
Mitigation: Review install.sh before running it, keep cron disabled when continuous operation is not intended, and run status or bias checks manually first. <br>
Risk: Stored learnings may contain sensitive or instruction-like entries that later shape agent responses. <br>
Mitigation: Periodically review or delete memory/subconscious and .learnings content, sanitize sensitive entries, and inspect active biases before relying on them. <br>
Risk: Automatic promotion can turn pending learnings into live biases before they have been manually reviewed. <br>
Mitigation: Remove --enable-promotion from the rotate job until stored learnings and governance behavior have been inspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/elyasdruid/subconscious) <br>
- [README](README.md) <br>
- [Architecture Reference](references/ARCHITECTURE.md) <br>
- [Installation Guide](references/INSTALL.md) <br>
- [Learnings Bridge Wiring](references/WIRING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; scripts maintain local JSON and JSONL state files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install scheduled cron jobs and maintain local memory under memory/subconscious.] <br>

## Skill Version(s): <br>
1.8.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
