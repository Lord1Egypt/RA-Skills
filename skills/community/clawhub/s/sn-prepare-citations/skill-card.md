## Description:

用于终稿完成且脚注需要后处理时：去重 [^key] 引用，转换为 [N] 编号，并追加参考文献。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and report-generation agents use this skill after a sn-deep-research draft is stitched to convert source footnotes into numbered references, insert optional L0 and table-of-contents sections, and produce final citation metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Legacy compatibility mode can overwrite the input report passed with --report.

Mitigation: Use the documented --output argument to write a separate report file, and keep a backup when legacy overwrite mode is required.

Risk: Unresolved orphan citations or claim-id citation leakage can leave unsupported references in the final report.

Mitigation: Treat non-empty orphan_citations or claim_id_leakage.unresolved status as a handoff blocker for writer or stitcher correction before delivery.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report output plus JSON citation status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a processed report and citations.json; stdout reports citation warnings, unresolved orphan citations, claim-id leakage status, and L0/TOC rendering status.]

## Skill Version(s):

2026.8.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
