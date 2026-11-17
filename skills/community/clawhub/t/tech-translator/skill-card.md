## Description:

Professional technical documentation translation expert, proficient in internet industry terminology. Translates user-provided files, preserves original formatting, and performs professional accuracy and format validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and documentation teams use this skill to translate technical documentation, API docs, READMEs, technical blogs, and specification files while preserving structure, code, links, placeholders, and terminology consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Folder mode may process sensitive files such as `.env`, credentials, private keys, or hidden configuration files.

Mitigation: Run folder translation only on reviewed directories and exclude sensitive or hidden configuration files before use.

Risk: URL mode may fetch internal systems or URLs that contain tokens.

Mitigation: Use URL mode only with public or approved URLs and remove tokens or secrets from URLs before translation.

Risk: Translated files are created in the workspace.

Mitigation: Review output paths and generated files before committing, sharing, or deploying workspace contents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/tech-translator)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Translated files in the original or detected format, plus a concise text validation summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes translated outputs to the workspace root and preserves supported file structures where applicable.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
