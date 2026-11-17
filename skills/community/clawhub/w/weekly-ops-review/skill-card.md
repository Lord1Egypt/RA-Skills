## Description:

Turn scattered notes, metrics, and unfinished tasks into a weekly operating review with wins, misses, blockers, and next-week priorities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, operators, and team leads use this skill to turn weekly notes, metrics, task lists, calendar highlights, and goals into a concise operating review with wins, misses, blockers, decisions, and next-week priorities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may organize incomplete or ambiguous user-provided operational data into a review that looks more certain than the inputs support.

Mitigation: Keep assumptions explicit, avoid fabricating metrics or evidence, and mark uncertain fields for confirmation.

Risk: The helper script can create or overwrite its configured local JSON output file.

Mitigation: Run it only on intentional inputs and choose an output path the user is comfortable creating or replacing.

Risk: Broad natural-language trigger phrases could activate the skill unintentionally in automated deployment environments.

Mitigation: Narrow trigger phrases where automatic activation is enabled.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/weekly-ops-review)
- [Publisher Profile](https://clawhub.ai/user/52yuanchangxing)
- [README](artifact/README.md)
- [Review Template](artifact/resources/review_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown review memo and action board, with optional JSON draft output from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script writes a local JSON draft to an explicit output path.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
