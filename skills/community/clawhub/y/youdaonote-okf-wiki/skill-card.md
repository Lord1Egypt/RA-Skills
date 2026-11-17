## Description:

YoudaoNote OKF Wiki helps agents create, maintain, query, lint, archive, and export OKF v0.1 knowledge bases in YoudaoNote using cloud-backed Markdown notes and OKF frontmatter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lephix](https://clawhub.ai/user/lephix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and knowledge workers use this skill to manage portable OKF knowledge bases in YoudaoNote, including ingestion, cross-linking, conformance checks, query synthesis, conversation archiving, and local bundle export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs persistent writes to a user's YoudaoNote account and may update OKF metadata automatically.

Mitigation: Use it only with an account and knowledge base the user intends the agent to modify; require explicit confirmation before bulk updates or initialization.

Risk: Credential and API-key handling is under-scoped in the security evidence.

Mitigation: Prefer secure credential entry when the CLI supports it, avoid shared machines for setup, and do not expose API keys in chat or saved notes.

Risk: Export operations write local files and can place knowledge-base content in an unintended path.

Mitigation: Confirm export destinations before writing and review generated local files before committing or sharing them.

Risk: Temporary-file handling is called out as an area needing improvement.

Mitigation: Use private working directories where possible and remove temporary OKF files after the CLI operation completes.

## Reference(s):

- [YoudaoNote homepage](https://note.youdao.com)
- [OKF v0.1 specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
- [OKF spec summary](references/okf-spec-summary.md)
- [YoudaoNote CLI install guide](https://note.youdao.com/help-center/cli-install-guide.html)
- [ClawHub skill page](https://clawhub.ai/lephix/skills/youdaonote-okf-wiki)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and structured status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update YoudaoNote notes and local OKF bundle files after user authorization.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
