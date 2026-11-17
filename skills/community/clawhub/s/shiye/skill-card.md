## Description:

师爷 is a three-model review skill that uses Kimi, GLM, and Qwen to assess documents, code, resumes, and other text, then returns score comparisons, issue details, consensus findings, and improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vlarkspur](https://clawhub.ai/user/vlarkspur)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, reviewers, and other external users can use this skill to cross-review text artifacts such as documents, source code, resumes, emails, notices, and presentation content. It is intended to compare model judgments and highlight low-scoring items that need human follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewed content may be sent to a configured external model API.

Mitigation: Use only approved HTTPS endpoints, avoid confidential or regulated content unless approved, and confirm user consent before sending content outside the local environment.

Risk: API credentials can be placed directly in the source file.

Mitigation: Prefer the SHIYE_API_KEY environment variable, use a limited-scope key, and avoid committing real credentials into the artifact.

Risk: Generated scores and consensus findings can be misleading or incomplete.

Mitigation: Treat the three-model output as review assistance and require human review before acting on low scores, disputed findings, or improvement suggestions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vlarkspur/skills/shiye)
- [Publisher profile](https://clawhub.ai/user/vlarkspur)
- [Configured model API endpoint](https://api.deepseek.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with terminal text tables and JSON model-response parsing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reviews up to 16000 characters of supplied content and may call the configured external model API.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
