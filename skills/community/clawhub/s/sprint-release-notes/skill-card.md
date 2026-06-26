## Description: <br>
Automatically generates sprint release notes from a GitHub Project Board, groups completed work by repository, and can publish per-repository Markdown release bodies to GitHub Releases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenkus47](https://clawhub.ai/user/tenkus47) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering leads use this skill to turn completed GitHub Project Board sprint items into release-note drafts, contributor summaries, and optional GitHub Release publications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can use a GitHub token with repository and project authority to read project data and publish release content. <br>
Mitigation: Use a fine-grained token limited to the exact project and repositories needed, run with dry-run first, and require explicit approval before publishing releases or comments. <br>
Risk: The bundled configuration example stores a PAT placeholder in YAML, which could encourage plaintext credential storage. <br>
Mitigation: Provide tokens through a secret manager or environment variable and avoid committing real PATs, webhook URLs, or generated config files. <br>
Risk: Generated release notes and contributor rankings may be incomplete or misleading if project items, labels, PR links, or scoring signals are sparse. <br>
Mitigation: Review generated Markdown, contributor callouts, and repository mappings before publishing them to GitHub Releases. <br>
Risk: The artifact contains both per-repository release publishing behavior and a repository file-commit path, which can broaden write impact if reused incorrectly. <br>
Mitigation: Keep execution scoped to the intended release path, remove unused commit-to-repo paths when packaging for deployment, and verify target repositories before running without dry-run. <br>


## Reference(s): <br>
- [GitHub API Queries Reference](artifact/references/github-queries.md) <br>
- [Contributor Scoring Reference](artifact/references/contributor-scoring.md) <br>
- [Sample Sprint Release Notes](artifact/scripts/sprint-33-2026-03-26.md) <br>
- [ClawHub Skill Listing](https://clawhub.ai/tenkus47/sprint-release-notes) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown release notes with optional shell/API execution guidance and local output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update GitHub Releases and may write a local Markdown copy when executed with a GitHub token.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
