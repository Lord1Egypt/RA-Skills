## Description:

Yiliu is an AI-powered note-taking knowledge base with semantic search, auto-summarization, and version management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[damingdong](https://clawhub.ai/user/damingdong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Yiliu to capture personal notes, search them semantically, manage note history, and export Markdown backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private note content and search terms may be sent to a configured AI provider when API-backed AI features are enabled.

Mitigation: Leave OPENAI_API_KEY unset for the most local behavior, or use only a trusted provider and avoid storing highly sensitive secrets in notes.

Risk: A custom AI endpoint could expose note content or search terms to an untrusted service.

Mitigation: Set OPENAI_BASE_URL only to a trusted HTTPS endpoint.

Risk: Delete commands can permanently remove notes and associated vectors.

Mitigation: Export Markdown backups before deleting important notes and treat delete operations as irreversible.

Risk: Dependency updates may change local model, storage, or AI-provider behavior.

Mitigation: Review dependency changes and rebuild/test the skill before deployment.

## Reference(s):

- [Yiliu ClawHub Skill Page](https://clawhub.ai/damingdong/skills/yiliu)
- [README](README.md)
- [Changelog](CHANGELOG.md)
- [MVP Development Log](docs/dev-log.md)
- [V1.2 Development Log](docs/v1.2-dev-log.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text responses, Markdown exports, and setup or configuration commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write local note data, vector indexes, and Markdown export files in the configured data directory.]

## Skill Version(s):

1.2.3 (source: server release metadata and package.json; artifact frontmatter and changelog list 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
