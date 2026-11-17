## Description:

Finds TikTok Shop creators who have promoted a specified product using Qinghu's product-creator lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and marketers use a TikTok Shop product ID to identify creators who have promoted that product, including for competitor research and creator outreach. Detailed creator profiles require a separate lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing third-party command-line tooling and storing or using a Qinghu access token may expose account credentials.

Mitigation: Confirm the qhkit package and Qinghu account workflow are trusted before installation; handle the token securely.

Risk: Product IDs are sent to Qinghu's service, and paid lookups can consume credits.

Mitigation: Confirm data-sharing suitability, check the current credit estimate, and obtain consent before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-tiktok-product-creators)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Concise creator-list summary or tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a product ID and Qinghu credentials; creator details require another lookup. Paid queries consume Qinghu credits.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
