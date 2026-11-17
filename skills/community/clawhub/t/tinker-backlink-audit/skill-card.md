## Description:

Discovers inbound links to a domain, subdomain, or GitHub repository and classifies each source as ours, organic, or ambiguous using GitHub referrers, supplied URLs, backlinks.sh, or Google Search Console CSV exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and growth operators use this skill to audit inbound links, separate self-created links from organic references, and refresh backlink counts for owned web properties or repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional network sources may contact GitHub through gh or backlinks.sh, and backlinks.sh usage may incur paid API calls.

Mitigation: Choose offline sources when possible, confirm backlinks.sh cost exposure before using that source, and provide the API key only through the environment or OS keychain.

Risk: Stored backlink API credentials may remain valid after local removal.

Mitigation: Use --logout to clear local storage and rotate or delete the key in the backlinks.sh account when access should be revoked.

Risk: The shipped allowlist and history dataset are examples from the publisher and can misclassify or pollute metrics if reused unchanged.

Mitigation: Replace the allowlist and historical series with data for the user's own owned surfaces before using write options.

Risk: Opt-in write modes can update local OpenClaw state or control-panel history.

Mitigation: Run without --write-state or without build-history --yes to preview output, then enable writes only for intended targets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/globalcaos/skills/tinker-backlink-audit)
- [Backlink sources reference](references/sources.md)
- [backlinks.sh API](https://api.backlinks.sh/v1/backlinks)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional terminal or JSON audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce ours, organic, and ambiguous backlink counts; optional write modes update local OpenClaw state or control-panel history only when requested.]

## Skill Version(s):

1.1.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
