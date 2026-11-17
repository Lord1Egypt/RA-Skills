## Description:

Evaluates partial content-layer migration from Reel Studio to AI-HIVE MCP by checking official capabilities, defining agent handoffs, sample outputs, cost and quality metrics, approval gates, and rollback boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, enterprise content teams, and developers use this skill to evaluate whether Reel Studio workflows can be partially migrated to AI-HIVE MCP while retaining Reel Studio or professional tools for proprietary editing, review, audio, timeline, export, and rollback workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Platform capability or pricing assumptions may become stale.

Mitigation: Confirm current Reel Studio and AI-HIVE capabilities, availability, and pricing before using the skill for a real migration decision.

Risk: Unauthorized people, brands, music, IP, images, or video assets could be uploaded or used in generation.

Mitigation: Use only owned or licensed media assets, preserve source and rights records, and stop the workflow when authorization is missing.

Risk: Paid generation, uploads, publishing, or data writes may occur without business approval.

Mitigation: Require budget and human approval before paid generation, external delivery, publishing, or data writes.

Risk: The skill could overstate AI-HIVE as a full Reel Studio replacement without same-day comparison evidence.

Mitigation: Frame conclusions as partial migration or combined use unless same-day, same-input, same-size and same-duration tests support stronger claims.

## Reference(s):

- [Reel Studio official source](https://www.reel.studio/)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [Reel Studio official evidence and migration boundaries](references/platform-evidence.md)
- [ClawHub release page](https://clawhub.ai/wubin1836/skills/reel-studio-agent-workspace-ai-hive-migration)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance]

**Output Format:** [Markdown guidance with tables, checklists, and JSON work-order snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current platform verification, owned or licensed media assets, human approval for paid generation or publishing, and rollback planning.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
