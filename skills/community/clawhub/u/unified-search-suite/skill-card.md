## Description:

Unified Search Suite routes agent web lookups through deep multi-source search, legacy merged search, thread tracing, URL-to-Markdown extraction, and MinerU document parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccmxigua](https://clawhub.ai/user/ccmxigua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill for current web research, fact checking, issue and PR thread tracing, and converting web pages or documents into traceable Markdown outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts multiple third-party search, model, and extraction APIs.

Mitigation: Constrain enabled providers and credentials before deployment, and run the skill behind network egress controls when handling sensitive work.

Risk: The skill can fetch arbitrary URLs from the user's machine network context.

Mitigation: Avoid internal-only URLs, secrets, private documents, and regulated data unless access and outbound destinations are explicitly controlled.

Risk: The skill writes extracted documents and parsing outputs to the local OpenClaw workspace.

Mitigation: Review workspace retention and cleanup practices before using the skill with confidential or regulated content.

Risk: The skill may use local GitHub credentials automatically to improve issue and pull request fetching.

Mitigation: Use scoped tokens or disable credential availability when fetching untrusted or unnecessary repository content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ccmxigua/skills/unified-search-suite)
- [Unified Search report template](artifact/references/report-template.md)
- [Search intent guide](artifact/vendor/openclaw-search-skills/search-layer/references/intent-guide.md)
- [Authority domains reference](artifact/vendor/openclaw-search-skills/search-layer/references/authority-domains.json)
- [Content extraction heuristics](artifact/vendor/openclaw-search-skills/content-extract/references/heuristics.md)
- [Content extraction domain whitelist](artifact/vendor/openclaw-search-skills/content-extract/references/domain-whitelist.md)
- [MinerU API docs](https://mineru.net/apiManage/docs)
- [MinerU output files](https://opendatalab.github.io/MinerU/reference/output_files/)
- [OpenClaw runtime](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON result contracts, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source links, extracted document paths, consensus findings, uncertainty, and next-step guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
