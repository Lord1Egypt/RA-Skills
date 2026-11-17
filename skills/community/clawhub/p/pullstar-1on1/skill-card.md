## Description:

Generate a 1-on-1 brief from GitHub activity using a deterministic five-step agent pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacksync](https://clawhub.ai/user/jacksync)

### License/Terms of Use:

MIT-0

## Use Case:

Engineering managers and team leads use this skill to turn an engineer's GitHub pull request and review activity into a concise preparation brief for a 1-on-1. It supports data-backed conversation preparation without presenting the result as a performance review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles GitHub tokens and can read repositories visible to the configured token.

Mitigation: Use a fine-grained token where possible, or a narrowly scoped classic token with GITHUB_ORG set to limit ingestion scope.

Risk: PR insights mode may send private pull request discussion text to the configured LLM provider.

Mitigation: Leave PR insights disabled unless raw PR discussions are appropriate for the provider, and review llm_input_<login>.json before inference.

Risk: Local .pullstar artifacts may contain private engineering activity data.

Mitigation: Review and delete generated .pullstar artifacts when they may contain private data.

Risk: Runtime dependencies may change behavior if installed without version pinning.

Mitigation: Use an isolated Python environment with pinned dependencies where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jacksync/skills/pullstar-1on1)
- [Publisher profile](https://clawhub.ai/user/jacksync)
- [GitHub classic personal access tokens](https://github.com/settings/tokens)
- [GitHub fine-grained personal access tokens](https://github.com/settings/personal-access-tokens)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown brief embedded in JSON artifacts, with command guidance for the agent workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local .pullstar artifacts for ingest, scoring, LLM input, LLM output, and final output; PR insights mode may include bounded raw PR discussion excerpts.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
