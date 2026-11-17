## Description:

AI-powered X/Twitter search for real-time trends, breaking news, sentiment analysis, and social media insights, with paid requests via the x402 protocol on Base network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tzannetosgiannis](https://clawhub.ai/user/tzannetosgiannis)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to run paid X/Twitter searches for real-time trends, sentiment, viral content, hashtags, and public opinion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a wallet private key, which can expose funds if the key is stored insecurely or shared with an unsafe workflow.

Mitigation: Use a dedicated low-balance wallet, avoid storing the key in a project directory, and restrict any config file to the current user.

Risk: The search script runs an unpinned npx package, so the executed package can change between searches.

Mitigation: Review the package source and behavior before use, and treat each run as executing third-party code that may have changed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tzannetosgiannis/skills/x-search-x402)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell commands and search-result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid searches require a configured x402 wallet private key and sufficient USDC on Base network.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
