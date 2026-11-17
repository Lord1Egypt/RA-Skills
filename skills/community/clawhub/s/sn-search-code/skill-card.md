## Description:

Searches developer resources across GitHub, Stack Overflow, Hacker News, and Hugging Face for code examples, open-source projects, issues, technical Q&A, discussions, models, datasets, and Spaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to locate relevant code, project, issue, Q&A, discussion, model, dataset, and Space results while working on implementation or research tasks. It provides runnable search helpers and normalized result output for downstream review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to selected third-party developer APIs.

Mitigation: Avoid submitting sensitive private text unless disclosure to that API provider is acceptable.

Risk: Optional API tokens can be exposed if passed directly on the command line or included in logs.

Mitigation: Provide credentials through environment variables or a secret manager, and avoid storing real secrets in skill payloads, reports, logs, or commits.

Risk: The Python dependency is specified as a lower-bounded package version.

Mitigation: Install in an isolated Python environment and consider pinning httpx before production use.

## Reference(s):

- [GitHub Search API](https://api.github.com/search)
- [Stack Exchange Advanced Search API](https://api.stackexchange.com/2.3/search/advanced)
- [Algolia Hacker News Search API](https://hn.algolia.com/api/v1)
- [Hugging Face Hub API](https://huggingface.co/api)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; helper scripts return JSON search results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires httpx; search scripts call third-party developer APIs and may use optional credentials from CLI arguments or environment variables.]

## Skill Version(s):

2026.8.19 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
