## Description:

Twitter/X.com data access for agents to search tweets, look up user profiles, and retrieve recent tweets through the Vincent credit system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glitch003](https://clawhub.ai/user/glitch003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give agents Twitter/X lookup capabilities for tweet search, tweet retrieval, profile lookup, and recent user-tweet retrieval. It is suited for workflows that can tolerate paid per-call access, persisted Vincent data-source credentials, and human-controlled credit management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and persist a Vincent DATA_SOURCES key for paid data access.

Mitigation: Use a dedicated account or key, store credentials only in the declared config paths, and revoke access from the Vincent frontend when no longer needed.

Risk: The skill can run a mutable npm CLI and make paid API calls.

Mitigation: Pin the Vincent CLI version where possible, review commands before execution, and set explicit spending controls before enabling agent use.

Risk: The skill supports wallet-funded credit purchases through an autonomous top-up flow.

Mitigation: Require clear user approval before any top-up and use a low-balance dedicated wallet if payment automation is enabled.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/glitch003/skills/vincent-twitter)
- [Vincent Homepage](https://heyvincent.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include tweet or profile JSON and Vincent credit metadata such as per-call cost and remaining credit.]

## Skill Version(s):

1.0.69 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
