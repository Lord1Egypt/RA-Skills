## Description:

The supplied skill guides agents through collecting public Apple App Store data with SocQ, despite this release being labeled as Snapchat research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[socq](https://clawhub.ai/user/socq)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and developers can use the supplied instructions to collect and analyze public Apple App Store app details, reviews, and rankings with SocQ. Verify the release contents before using it for Snapchat research: the packaged instructions target Apple App Store instead.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The listed Snapchat release contains Apple App Store instructions and endpoints.

Mitigation: Confirm the package contents and obtain the intended Snapchat skill before submitting Snapchat research requests.

Risk: SocQ receives submitted public data and uses an API credential for requests.

Mitigation: Confirm trust in SocQ, keep SOCQ_API_KEY out of prompts and URLs, and apply API-key rate, credit, and IP limits.

Risk: The npx fallback may install an unpinned CLI version, and large collections may incur credits.

Mitigation: Install a known @socq/cli version and review expected costs before approving large paid runs.

## Reference(s):

- [ClawHub release listing](https://clawhub.ai/socq/skills/socq-snapchat-research)
- [SocQ Apple App Store API documentation (packaged platform)](https://docs.socq.ai/api-manual/apple-app-store)
- [SocQ MCP and CLI integration guide](https://docs.socq.ai/integrations/overview)
- [Packaged platform reference](artifact/references/platform.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with research findings and optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include endpoint, request scope, credit use, task status, result count, pagination coverage, and raw export location.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
