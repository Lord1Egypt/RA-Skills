## Description:

Get reports from a Sure personal financial board.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bt0r](https://clawhub.ai/user/bt0r)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure Sure API access and retrieve personal financial account amounts through a user-directed API request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent query Sure financial account data.

Mitigation: Install it only when that access is intended, and review retrieved account information before sharing or storing it elsewhere.

Risk: A Sure API key or untrusted base URL could expose account data.

Mitigation: Keep SURE_API_KEY private, use a trusted SURE_BASE_URL, and prefer a limited or revocable API key if Sure supports one.

## Reference(s):

- [Sure homepage](https://sure.am)
- [ClawHub skill page](https://clawhub.ai/bt0r/skills/sure)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl with SURE_API_KEY and SURE_BASE_URL environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
