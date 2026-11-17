## Description:

Looks up TikTok shopping livestreams associated with a product ID using 青虎AI data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

TikTok Shop sellers and analysts use this skill to find livestreams associated with a product and review its live-selling activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install Node and qhkit, change the local PATH, and configure an access token without a separate setup decision.

Mitigation: Ask for explicit approval before installing dependencies, changing the local environment, or configuring credentials; avoid exposing the token.

Risk: Product-live lookups consume paid credits, and the final charge can increase with the number of results.

Mitigation: Estimate the cost and obtain consent before paid calls; limit result volume and report the credits actually charged.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-tiktok-product-lives)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Natural-language summary of product-associated livestream listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report credits consumed for paid lookups.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
