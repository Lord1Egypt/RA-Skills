## Description:

Professional search (news, places, maps, reviews, scholar, patents) and bulk scraping via Serper API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vinitngr](https://clawhub.ai/user/vinitngr)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run Serper-backed web, news, places, maps, shopping, scholar, patent, and scraping workflows from command-line prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global npm installation can introduce supply-chain risk, especially when forced installation is used.

Mitigation: Install a pinned reviewed version, avoid --force when possible, and remove the global package when it is no longer needed.

Risk: Serper API credentials are required and may be exposed or overused if handled carelessly.

Mitigation: Use a revocable Serper API key with limited quota and verify where the CLI stores credentials before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vinitngr/skills/serper-v)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on Serper API responses and the selected endpoint, query, locale, date range, page, and limit.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
