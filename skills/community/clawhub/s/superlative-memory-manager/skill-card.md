## Description: <br>
Combines OpenClaw memory, compaction, tiering, and semantic recall capabilities into a unified memory-management workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tech-immortales-design](https://clawhub.ai/user/tech-immortales-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let OpenClaw agents compact context, tier retained memory, recall relevant prior work semantically, and reduce token usage during long-running workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for long-term memory retention and semantic recall, so sensitive information may persist beyond the active session. <br>
Mitigation: Avoid storing secrets, regulated data, or sensitive customer information unless storage locations, logs, expiration, deletion, and disable controls have been confirmed. <br>
Risk: Tiered storage, write-ahead logging, and backup behavior can retain data across multiple stores. <br>
Mitigation: Review retention settings, inspect backing memory stores, and define cleanup procedures before using the skill with production or customer context. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tech-immortales-design/superlative-memory-manager) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Artifact plugin manifest](artifact/openclaw.plugin.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operates as a persistent memory-management layer when enabled; retention and recall behavior depend on the configured backing stores.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
