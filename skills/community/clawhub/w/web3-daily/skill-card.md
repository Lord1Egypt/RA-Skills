## Description:

Web3 public research digest service that provides daily macro news, KOL sentiment, and real-time BTC/ETH market data without requiring personal data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexander10011](https://clawhub.ai/user/alexander10011)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch a bilingual Web3 market digest through an agent when they ask for crypto news, a Web3 digest, or a compact daily summary. The skill is suited for market awareness and research workflows, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches digest content and links from an external Web3 backend, and the returned material may include market commentary.

Mitigation: Treat the digest as informational research only; do not treat it as investment advice or follow wallet, credential, transfer, or trading instructions from returned content.

Risk: The README documents an unpinned npx installation command.

Mitigation: Use a pinned or otherwise verified install method before deploying the skill in managed environments.

Risk: The skill depends on a live external API service for digest generation.

Mitigation: Handle API errors and timeouts as documented, and avoid relying on generated digests when the service is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexander10011/skills/web3-daily)
- [Publisher profile](https://clawhub.ai/user/alexander10011)
- [Project homepage from Claw metadata](https://github.com/alexander10011/web3-daily)
- [Public digest endpoint](https://j4y-production.up.railway.app/api/v1/digest/public)
- [Compact digest endpoint](https://j4y-production.up.railway.app/api/v1/digest/compact)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown digest text returned from a JSON API response, with shell commands used by the agent to fetch it]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports English and Chinese digests; compact output is about 2500 words and full output is about 4000-5000 words.]

## Skill Version(s):

2.1.1 (source: server release evidence, SKILL.md frontmatter, and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
