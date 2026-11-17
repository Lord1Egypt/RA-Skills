## Description:

Evidence-driven material collection and organization workflow for Chinese content creation, covering planning, search, download, indexing, and reusable source-library maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gogoingai](https://clawhub.ai/user/gogoingai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and content teams use this skill to plan research, gather similar articles and factual materials, fetch pages through the Wenqu CLI when authorized, and organize sources into reusable libraries for later writing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default workflow may install and run an external CLI and managed browser stack that was not fully verifiable from the reviewed artifact.

Mitigation: Run the skill in a constrained environment, require explicit authorization before setup, and verify the CLI release version and digest before first use.

Risk: The skill may access the web for searches and page fetches and write a persistent materials library under the user's home directory.

Mitigation: Review the collection scope before execution, use explicit page limits for site fetches, and inspect generated material indexes and saved files before reuse.

## Reference(s):

- [Wenqu Library source homepage](https://github.com/gogoingai/wenqu-skills/tree/master/wenqu-library)
- [Wenqu skills repository](https://github.com/gogoingai/wenqu-skills)
- [Collection Playbook](references/collection-playbook.md)
- [Wenqu CLI](references/wenqu-cli.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with source tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update material indexes, fetched article files, and persistent reusable library entries when authorized.]

## Skill Version(s):

0.1.19 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
