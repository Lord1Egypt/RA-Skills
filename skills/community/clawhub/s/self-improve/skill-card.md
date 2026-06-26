## Description: <br>
Self-Improve is a pluggable framework that scans agent memory and feedback, extracts reusable learning rules, and proposes approval-gated improvements to agent system files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[don068589](https://clawhub.ai/user/don068589) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a scheduled self-improvement process that reviews agent memory logs, stores distilled knowledge, and queues proposed system-file changes for approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can repeatedly scan agent memories and store shared long-term outputs. <br>
Mitigation: Install only when a team-wide memory-learning system is intended, restrict workspace_root and knowledge_root before enabling Cron, and define retention, deletion, redaction, and per-agent consent rules. <br>
Risk: Distilled guidance or system-file proposals may preserve sensitive or incorrect information. <br>
Mitigation: Review proposals/PENDING.md before approval and scan proposed changes before applying them. <br>
Risk: Optional blog, publication, or broad knowledge outputs may expose information beyond the intended workspace. <br>
Mitigation: Disable unneeded modules and publication outputs unless they are explicitly required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/don068589/self-improve) <br>
- [Skill Overview](artifact/SKILL.md) <br>
- [System Documentation](artifact/SYSTEM.md) <br>
- [Engine Documentation](artifact/ENGINE.md) <br>
- [Runtime Mechanism](artifact/RUNTIME.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, YAML configuration, JSON/JSONL state, and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes scheduled run data, proposals, drafts, and knowledge files under configured storage roots; system-file changes are approval-gated.] <br>

## Skill Version(s): <br>
2.2.1 (source: server release metadata; artifact config reports 2.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
