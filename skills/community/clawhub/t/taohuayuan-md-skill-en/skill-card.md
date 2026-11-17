## Description:

Generates and manages local files that persist an autonomous agent's physical anchor, identity record, short-term interaction log, and consolidated long-term memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a local, physically anchored memory record to an autonomous agent. It is intended for environments where interaction history and physical-context data should remain on the host or edge node.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist broad user interaction history and physical-context information in local memory files.

Mitigation: Keep the storage directory private, avoid recording secrets or precise personal data, and review memory entries before consolidation or reuse.

Risk: Persistent memories may be reused by another agent without adequate consent or filtering.

Mitigation: Require explicit review before loading, sharing, or consolidating memory files across agents.

Risk: The release evidence flags missing clear deletion and consent controls for retained local memory.

Mitigation: Define a retention and deletion process before deployment, and give users a way to inspect and remove stored memories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/taohuayuan-md-skill-en)
- [README](readme.md)
- [Taohuayuan.md V2.0 whitepaper](taohuayuan_md_whitepaper_en.md)
- [Sample taohuayuan.md record](samples/taohuayuan.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python-generated local Markdown and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local taohuayuan.md, hippocampus_logs.json, and memory_files outputs when run.]

## Skill Version(s):

2.0.0 (source: server release metadata, package.json, changelog released 2026-05-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
