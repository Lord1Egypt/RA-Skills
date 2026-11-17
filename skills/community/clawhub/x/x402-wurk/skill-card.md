## Description:

Hire humans for microjobs such as feedback, opinions, and small tasks, and buy social growth services paid with USDC via x402 on Solana or Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[statikheadz](https://clawhub.ai/user/statikheadz)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to create paid agent-to-human microjobs, retrieve human submissions, and purchase social growth services through x402 payment flows. Use requires explicit approval for paid actions and careful handling of job secrets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger paid USDC transactions for microjobs and social growth services.

Mitigation: Use only for explicit, user-approved paid tasks and verify the service, destination URL or handle, network, amount, and total USDC cost before signing.

Risk: Social growth and vote services may violate platform rules or user expectations.

Mitigation: Avoid social-growth, engagement, or vote-buying uses unless the user has approved the action and the use is permitted by the relevant platform.

Risk: The artifact documents curl-based installation from remote URLs.

Mitigation: Do not install with remote curl commands unless the downloaded files are independently verified against trusted release evidence.

Risk: Returned job secrets act as bearer tokens for retrieving submissions.

Mitigation: Treat secrets like passwords and avoid exposing them in shared URLs, logs, shell history, or plaintext state files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/statikheadz/skills/x402-wurk)
- [WURK website](https://wurk.fun)
- [WURK API](https://wurkapi.fun)
- [WURK x402 discovery](https://wurkapi.fun/.well-known/x402)
- [WURK X/Twitter](https://x.com/WURKDOTFUN)
- [WURK Telegram](https://t.me/WURKCREATORS)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, API calls]

**Output Format:** [Markdown with inline bash, TypeScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes x402 payment workflow examples, endpoint guidance, and secret-handling instructions.]

## Skill Version(s):

1.0.0 (source: server release; artifact frontmatter, package.json, and CHANGELOG report 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
