## Description:

ThetaEdge Skill enables agents to use the Thetix options intelligence API for portfolio analysis, market data, dashboard widgets, options opportunities, brokerage account lookup, and AI-generated trading ideas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mempko](https://clawhub.ai/user/mempko)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect an agent to ThetaEdge for finance, investing, trading, portfolio, options, market data, dashboard, and trading-idea workflows. It can retrieve and summarize account-scoped data and propose or manage dashboard and opportunity actions through authenticated API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses sensitive ThetaEdge API credentials.

Mitigation: Use a limited API key where possible, keep credentials out of shared logs and transcripts, and avoid printing API keys during troubleshooting.

Risk: Finance and options workflows may have financially consequential effects.

Mitigation: Require explicit final user confirmation before opportunity actions, dismissals, deletions, or other state-changing requests.

Risk: The VM setup helper runs remote installers and system package changes.

Mitigation: Review the setup script before execution and run it only in a trusted, isolated environment.

## Reference(s):

- [Thetix API Reference](artifact/reference.md)
- [ThetaEdge Skill README](artifact/README.md)
- [OpenClaw VM Setup](artifact/docs/vm-setup.md)
- [ThetaEdge Application](https://app.thetaedge.com)
- [ThetaEdge API Base](https://api.thetaedge.ai)
- [ClawHub Skill Page](https://clawhub.ai/mempko/skills/thetaedge-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, tables, JSON snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires THETAEDGE_API_KEY; THETAEDGE_API_BASE is optional and defaults to https://api.thetaedge.ai.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
