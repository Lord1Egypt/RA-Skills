## Description:

Builds evidence-only Kimball semantic layers from APIs, CLIs, or tables with an HTML decision workbench and emits OKF or YAML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenticweb4](https://clawhub.ai/user/agenticweb4)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to turn REST/OpenAPI, CLI, table, or DDL contracts into governed semantic layers with explicit review gates. It supports operation inventories, semantic modeling decisions, OKF or YAML outputs, and verification reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated local review HTML can run injected script if untrusted interface text is embedded unsafely.

Mitigation: Review or patch the HTML generation path to HTML-safely encode model JSON or store it outside the script element, and open generated reports only from trusted inputs until fixed.

Risk: Semantic models may contain incorrect grain, dimensions, measures, or routing when source contracts are incomplete or ambiguous.

Mitigation: Keep the skill's evidence-only and explicit approval gates in place; unresolved modeling gaps should remain TODO(verify) items or return to review instead of being silently accepted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agenticweb4/skills/semantic-creator)
- [Phase 1 Ingest](artifact/references/ingest.md)
- [Phase 2 Review](artifact/references/review.md)
- [Phase 3 Emit OKF](artifact/references/emit-okf.md)
- [Phase 3 Emit YAML](artifact/references/emit-yaml.md)
- [Phase 4 Verify](artifact/references/verify.md)
- [Worked Example](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown, JSON, HTML, YAML, and verification summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an offline review workbench before emitting OKF or YAML files; final semantic-layer output is gated on explicit user approval.]

## Skill Version(s):

0.5.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
