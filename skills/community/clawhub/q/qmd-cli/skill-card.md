## Description:

Search and retrieve Markdown documents from local knowledge bases using qmd, including BM25 keyword search, vector semantic search, hybrid LLM re-ranking, and document retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dpaluy](https://clawhub.ai/user/dpaluy)

### License/Terms of Use:


## Use Case:

Developers, researchers, and knowledge workers use this skill to query indexed Markdown notes, documentation, meeting transcripts, and similar local knowledge bases through qmd.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs a mutable third-party GitHub dependency without a pinned commit or integrity check.

Mitigation: Install only from a trusted qmd upstream source, preferably pinning a commit and using an isolated environment.

Risk: qmd can index and return full local Markdown document contents.

Mitigation: Add only the Markdown directories intended for search and avoid broad retrieval options unless full document content is needed.

## Reference(s):

- [QMD CLI ClawHub page](https://clawhub.ai/dpaluy/skills/qmd-cli)
- [qmd upstream repository](https://github.com/tobi/qmd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON CLI output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires qmd CLI installation; qmd invocations should use --json; vector search and query modes can have about 1 minute cold start latency.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
