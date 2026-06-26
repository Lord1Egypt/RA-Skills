## Description: <br>
Provides autonomous agents with a local physical-anchor and persistent memory workflow that writes identity, interaction, preference, and environment context into local Markdown and JSON files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spacesq](https://clawhub.ai/user/spacesq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local, edge-hosted memory files that preserve an agent's physical anchor, short-term interaction cache, and consolidated long-term context. It is intended for agents that deliberately keep local state about interactions, preferences, and physical-environment observations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create long-term local memories from interactions, preferences, and physical-context data without clear consent or deletion controls. <br>
Mitigation: Require explicit opt-in, disable silent or background capture, and provide user-visible inspection and deletion for all generated memory files. <br>
Risk: Local memory files may contain sensitive personal, environmental, or operational details. <br>
Mitigation: Restrict captured sensor categories, redact secrets and personal data before writing, and protect generated files with local access controls and retention limits. <br>
Risk: Automatic memory consolidation may preserve inaccurate or unwanted entries as long-term context. <br>
Mitigation: Review consolidated memory files before reuse, allow users to remove entries, and avoid treating consolidated memories as authoritative without validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spacesq/taohuayuan-md-skill-cn) <br>
- [Publisher profile](https://clawhub.ai/user/spacesq) <br>
- [artifact/readme.md](artifact/readme.md) <br>
- [artifact/skill.md](artifact/skill.md) <br>
- [artifact/taohuayuan_md_whitepaper.md](artifact/taohuayuan_md_whitepaper.md) <br>
- [artifact/samples/taohuayuan.md](artifact/samples/taohuayuan.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown and JSON files with Python and shell usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local taohuayuan.md, hippocampus_logs.json, and memory_files/ outputs; no cloud processing is described.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and package.json; changelog top entry is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
