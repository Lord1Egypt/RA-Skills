## Description:

x-osv helps agents query the Google OSV database for package vulnerabilities and scan local projects for vulnerable dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwinjhlee](https://clawhub.ai/user/edwinjhlee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to look up OSV vulnerability data, scan local dependency files with osv-scanner, and generate SARIF-oriented security reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project scans may read local dependency files in the selected directory.

Mitigation: Run scans only on intended project paths and review the selected path before executing scan commands.

Risk: The skill depends on external tools, including x-cmd and osv-scanner, that are not bundled with the artifact.

Mitigation: Install dependencies from their official sources and verify they are available before using project-scanning commands.

Risk: Vulnerability lookup and scan results may be incomplete when unauthenticated rate limits or external service availability affect OSV queries.

Mitigation: Treat results as advisory security signals and confirm important findings with the referenced OSV data or scanner output.

## Reference(s):

- [OSV.dev](https://osv.dev)
- [osv-scanner](https://github.com/google/osv-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local project paths and external tools that must be installed separately.]

## Skill Version(s):

1.0.1 (source: server release metadata, changelog, and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
