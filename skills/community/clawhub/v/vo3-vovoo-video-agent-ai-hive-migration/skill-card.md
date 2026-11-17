## Description:

A Chinese-language workflow skill for evaluating a neutral workflow-rebuild migration from VO3 / Vovoo AI Video Agent to an agent-led AI-HIVE MCP media-generation process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to assess whether a VO3 / Vovoo AI Video Agent workflow can be rebuilt with a host agent plus AI-HIVE MCP, including official capability checks, pilot sample design, acceptance metrics, approval gates, and rollback criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded media, likenesses, product images, brands, music, or reference videos may lack sufficient rights for generation or reuse.

Mitigation: Confirm asset rights before upload, preserve source IDs and file hashes, and stop the workflow when unauthorized people, trademarks, IP, music, or reference video are found.

Risk: AI-HIVE tool schemas, model availability, and pricing can change before execution.

Mitigation: Run live tool discovery and capture same-day model and price snapshots before creating tasks or making cost claims.

Risk: Migration conclusions can become misleading if VO3 / Vovoo capabilities or AI-HIVE outputs are not rechecked with comparable inputs.

Mitigation: Revisit the official VO3 / Vovoo source before release and require same-day, same-input, same-duration acceptance tests before claiming replacement quality.

Risk: Automated spending, external sharing, or publication could occur before review.

Mitigation: Keep human approval gates for budgeted generation, publishing, external sharing, and data writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/vo3-vovoo-video-agent-ai-hive-migration)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [VO3 / Vovoo AI Video Agent official source](https://www.vo3ai.com/ai-video-agent)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [VO3 / Vovoo AI Video Agent 官方证据与迁移边界](references/platform-evidence.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with structured checklists, tables, and JSON work-order examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces migration assessment guidance, AI-HIVE MCP work-order structure, cost and quality metrics, human approval gates, and rollback criteria.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
