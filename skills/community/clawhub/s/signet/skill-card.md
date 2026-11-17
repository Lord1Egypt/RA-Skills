## Description:

Signet helps agents check spotlight ad prices, list current Signet ads, and place URL ads on the Signet spotlight through x402 payments on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebayaki](https://clawhub.ai/user/sebayaki)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect Signet spotlight pricing and activity, simulate paid placement, and post a URL advertisement through the Signet x402 flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running mutable third-party CLI code can change behavior between executions.

Mitigation: Pin and verify the CLI package version before use, and review the package before allowing it to create or submit payments.

Risk: Paid onchain posting requires wallet signing and can spend funds if parameters are wrong or misunderstood.

Mitigation: Use a dedicated low-value wallet, simulate first, and manually confirm destination, network, token, amount, URL, and guarantee hours before live submission.

Risk: Passing a raw private key through command-line options or environment variables can expose wallet credentials.

Mitigation: Prefer a protected signer or vault and avoid command-line private key arguments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sebayaki/skills/signet)
- [Signet API Base](https://signet.sebayaki.com)
- [Signet x402 Estimate Endpoint](https://signet.sebayaki.com/api/x402/estimate?guaranteeHours=0)
- [Signet Signature List Endpoint](https://signet.sebayaki.com/api/signature/list?startIndex=0&endIndex=5)
- [Signet x402 Spotlight Endpoint](https://signet.sebayaki.com/api/x402/spotlight)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes examples for estimating cost, listing current ads, simulating placement, and submitting paid spotlight posts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
