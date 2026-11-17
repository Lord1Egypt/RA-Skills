## Description:

Read-only Oracle SQL and live schema export for SimpleERP, supporting setup, schema reference generation, and SELECT/WITH/EXPLAIN PLAN queries through bundled npm scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icystssi-lang](https://clawhub.ai/user/icystssi-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and ERP support teams use this skill to inspect the SimpleERP Oracle schema, generate local schema references, run bounded read-only SQL reports, and summarize query results without performing database mutations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live Oracle credentials.

Mitigation: Use a dedicated least-privilege read-only Oracle account, do not pass passwords in chat, and avoid command-line password flags when a protected environment file can be used.

Risk: Local credential and query-result files may be exposed if file permissions or cleanup are weak.

Mitigation: Control permissions for .env and output files, keep generated outputs inside the skill output directory, and clean up files according to the deployment retention policy.

Risk: ERP query results may contain sensitive business or personal data.

Mitigation: Do not enable persistent memory for ERP data unless an approved retention policy exists, and review results before sharing them outside authorized channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/icystssi-lang/skills/simpleerp-db)
- [Bootstrap guide](references/bootstrap.md)
- [Tools reference](references/tools.md)
- [Playbook](references/playbook.md)
- [Table index](references/table-index.md)
- [Table reference](references/table-reference.md)
- [Table relationships](references/table-relationships.md)
- [Journal table pattern](references/journal-pattern.md)
- [node-oracledb documentation](https://node-oracledb.readthedocs.io/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with SQL snippets, shell commands, configuration guidance, and JSON query-result summaries when saved output is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are bounded by the Oracle user's database privileges and the skill's read-only query runner.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
