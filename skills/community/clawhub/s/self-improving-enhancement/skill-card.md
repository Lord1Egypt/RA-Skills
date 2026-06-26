## Description: <br>
Enhanced self-improvement skill with full chat logging for text and image metadata, smart memory compaction, automatic pattern recognition, context-aware learning, multi-skill synergy, visual statistics, and scheduled reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain local assistant memory, log conversations, compact recurring corrections, detect preference patterns, and produce periodic memory reviews. It is intended for users who intentionally want persistent local chat and memory records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local chat logs may retain sensitive user text or image metadata. <br>
Mitigation: Install only when persistent local logging is intended, avoid logging secrets or sensitive personal data, and review ~/self-improving/chat-logs regularly. <br>
Risk: Recent logs are protected from the built-in cleanup command for 30 days. <br>
Mitigation: Confirm that the 30-day retention behavior matches the deployment need before use and manage local files directly only under an approved retention process. <br>
Risk: The skill creates and updates local memory files under the user's home directory. <br>
Mitigation: Review ~/self-improving before deployment and include the directory in local data handling, backup, and deletion practices. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidme6/self-improving-enhancement) <br>
- [Publisher profile](https://clawhub.ai/user/davidme6) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact installation guide](artifact/INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python CLI commands and local Markdown, JSON, and JSONL files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local files under ~/self-improving, including chat logs, memory files, correction logs, and review state.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata; frontmatter changelog references V2.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
