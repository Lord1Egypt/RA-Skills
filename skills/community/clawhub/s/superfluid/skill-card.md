## Description:

Provides a knowledge base for the Superfluid Protocol, its smart contracts, integrations, and ecosystem workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kasparkallas](https://clawhub.ai/user/kasparkallas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to answer Superfluid Protocol questions, look up contract interfaces and integration patterns, and find the right SDK, API, subgraph, or command-line reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A balance lookup sends the wallet, token, and chain association to superapi.kazpi.com.

Mitigation: Use a trusted RPC when that association is sensitive.

Risk: Adapting financial examples without checking their parameters can affect token allowances or active streams; the DCA sample comment is stale.

Mitigation: Review recipients, amounts, allowances, and existing streams before adapting or executing an example.

Risk: The static review does not certify downloaded dependencies or deployed contracts.

Mitigation: Pin downloaded dependencies and independently review the packages and contracts used in an integration.

## Reference(s):

- [Protocol architecture](references/guides/architecture.md)
- [SDK guidance](references/guides/sdks.md)
- [API services](references/guides/api-services.md)
- [Command-line scripts](references/guides/scripts.md)
- [Smart contract patterns](references/guides/smart-contract-patterns.md)
- [CFAv1Forwarder contract interface](references/contracts/CFAv1Forwarder.abi.yaml)
- [GDAv1Forwarder contract interface](references/contracts/GDAv1Forwarder.abi.yaml)
- [Superfluid SDK documentation](https://sdk.superfluid.pro/docs)
- [Semantic Money Yellowpaper](references/deep-researches/semantic-money-yellowpaper.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code snippets, ABI details, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers are grounded in the skill's protocol references and may include integration caveats.]

## Skill Version(s):

1.2.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
