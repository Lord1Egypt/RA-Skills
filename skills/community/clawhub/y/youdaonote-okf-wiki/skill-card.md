## Description: <br>
YoudaoNote OKF Wiki helps agents create, maintain, query, lint, export, and archive OKF v0.1 knowledge bases stored in YoudaoNote. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lephix](https://clawhub.ai/user/lephix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to let an agent manage a YoudaoNote-backed OKF knowledge base, including initialization, ingestion, querying, consistency checks, export, and archival workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and update notes and folders in the configured YoudaoNote account. <br>
Mitigation: Use it only with the intended account and review prompts before initialization, ingest, archive, or any large batch write. <br>
Risk: The skill relies on the YoudaoNote CLI and API key configured by the user. <br>
Mitigation: Configure credentials only through the documented YoudaoNote CLI flow and rotate the API key if it is exposed. <br>
Risk: The skill can fetch user-provided URLs for ingest and write exported bundles to confirmed local paths. <br>
Mitigation: Provide only trusted source URLs and confirm export destinations before allowing file writes. <br>


## Reference(s): <br>
- [YoudaoNote](https://note.youdao.com) <br>
- [OKF v0.1 Specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) <br>
- [OKF v0.1 Spec Summary](references/okf-spec-summary.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured note content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the youdaonote CLI. The agent may read and write notes in the configured YoudaoNote account, ingest user-provided URLs, and export OKF bundles to user-confirmed local paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
