## Description:

Normalizes classification systems across teams or tables while preserving alias mappings and deprecated terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Data, analytics, and governance teams use this skill to turn category lists, aliases, and conflict notes into reviewable taxonomy-normalization drafts. It helps prepare current categories, overlaps, preferred categories, alias maps, deprecated terms, and migration suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the helper on broad directories may enumerate or summarize local text files beyond the intended input.

Mitigation: Run it only on files or directories intended for processing, and review the configured mode before using broad directory inputs.

Risk: Taxonomy-normalization drafts can incorrectly collapse meaningful business distinctions if applied without review.

Mitigation: Treat outputs as reviewable drafts and confirm mappings with domain owners before making production data or configuration changes.

Risk: Inputs may contain sensitive taxonomy, alias, or governance material.

Mitigation: Use local, authorized, and appropriately sanitized inputs, and choose output paths that match the data sensitivity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/taxonomy-normalizer)
- [README](artifact/README.md)
- [Skill specification](artifact/resources/spec.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or JSON reports generated from local inputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local files or inline text; the Python helper can write to a selected output path.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
