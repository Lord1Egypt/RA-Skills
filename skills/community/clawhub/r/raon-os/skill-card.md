## Description:

AI-powered startup companion for Korean founders. Evaluate business plans, match government funding programs (TIPS/DeepTech/Global TIPS), connect with 3,972+ TIPS-selected startups, get investor recommendations, and integrate with Kakao i OpenBuilder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifeissea](https://clawhub.ai/user/lifeissea)

### License/Terms of Use:

MIT-0

## Use Case:

External founders and startup operators use Raon OS to evaluate business plans, identify Korean government funding options, draft application materials, estimate valuation, and prepare investor-facing profiles.

### Deployment Geography for Use:

South Korea

## Known Risks and Mitigations:

Risk: The bundled server and widget have serious security issues, including path traversal, feedback authentication, XSS, request limit, and key-storage concerns.

Mitigation: Do not expose the server to a network or embed the widget in a trusted site until those issues are fixed and reviewed.

Risk: Local testing can involve API keys and business-plan content.

Mitigation: Use minimal dedicated API keys, avoid confidential business plans, and keep testing bound to localhost.

Risk: SaaS mode can send evaluation requests and extracted PDF text to the configured managed endpoint.

Mitigation: Configure only trusted endpoints and review data-handling requirements before processing sensitive business material.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lifeissea/skills/raon-os)
- [npm package](https://www.npmjs.com/package/@yeomyeonggeori/raon-os)
- [Raon OS homepage](https://k-startup.ai)
- [Government programs reference](references/gov-programs.md)
- [TIPS criteria reference](references/tips-criteria.md)
- [YC and a16z startup idea reference](references/yc-rfs.md)
- [Kakao i OpenBuilder setup](KAKAO_SETUP.md)
- [Web chat embed guide](widget/EMBED.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, CLI text, and REST API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save result files, return structured JSON, run a local HTTP API server, and provide Kakao/web widget responses.]

## Skill Version(s):

0.7.28 (source: frontmatter, package.json, release evidence, CHANGELOG released 2026-02-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
