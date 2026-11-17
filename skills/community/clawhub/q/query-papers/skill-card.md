## Description:

Retrieves relevant paper-kb knowledge-base content from a user's Gitea repository and helps produce Chinese answers with source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to search a personal Gitea-backed research knowledge base, read relevant pages, and answer questions with cited links. It is oriented toward stored papers, surveys, open-source projects, technical documents, experiment notes, and meeting notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests a Gitea site-admin token.

Mitigation: Use least-privilege credentials scoped only to the repositories and read operations needed for knowledge-base lookup.

Risk: The configured Gitea URL may use plain HTTP.

Mitigation: Require HTTPS for the Gitea endpoint before production or commercial use.

Risk: User questions may be persisted in query logs.

Mitigation: Make query logging explicit and optional, and avoid logging sensitive prompts or personal data.

Risk: Dependencies are specified with lower bounds rather than pinned versions.

Mitigation: Install pinned dependencies in an isolated virtual environment and review updates before deployment.

## Reference(s):

- [Query Papers on ClawHub](https://clawhub.ai/myd2002/skills/query-papers)
- [Publisher profile](https://clawhub.ai/user/myd2002)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Chinese Markdown answer with source links and inline shell commands for knowledge-base access]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses per-user context and Gitea-backed knowledge-base pages; query logging may persist user questions.]

## Skill Version(s):

2.1.1 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
