## Description:

Deal-sourcing scout for VCs running an AI-infrastructure thesis that fuses Hacker News, Product Hunt, web, Twitter/X, and LinkedIn signals through SELAT paid endpoints to produce a ranked startup shortlist with source links and outreach guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[selat-dev](https://clawhub.ai/user/selat-dev)

### License/Terms of Use:

MIT-0

## Use Case:

VC investors, scouts, and analysts use this skill to source AI-infrastructure companies, identify founders and teams with fresh market signals, and turn paid live-data responses into a ranked deal shortlist with links and an outreach note.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned globally installed SELAT CLI that manages wallet setup and paid API calls.

Mitigation: Install only after trusting the SELAT CLI publisher, prefer a pinned or isolated install when available, and review the installed package before use.

Risk: Running the workflow can spend USDC from the user's self-custody wallet through paid API endpoints.

Mitigation: Run the free dry-run first, review live quoted prices with the user, get explicit approval before wallet setup or paid execution, and keep wallet funding minimal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/selat-dev/skills/vc-ai-infra-scout)
- [SELAT skill homepage](https://github.com/SELAT-AI/selat-skills/tree/main/skills/vc-ai-infra-scout)
- [SELAT skills docs](https://github.com/SELAT-AI/selat-skills)
- [SELAT router](https://router.selat.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command blocks and a ranked shortlist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source links, ranking rationale, flags for teams with no announced round, and a short outreach note for the top pick.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
