## Description:

Looks up TikTok product-promotion videos associated with a product ID using Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and marketers use this skill to find videos associated with a TikTok product and review how others promote it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic installation or upgrades of unpinned tooling can change software running on the host.

Mitigation: Use a trusted, pre-provisioned, pinned qhkit version; require approval before installing or upgrading.

Risk: Host credential setup may overwrite an existing Qinghu token or mishandle secrets.

Mitigation: Use platform-managed secrets and require approval before changing existing credentials.

Risk: Paid video lookups can incur variable Qinghu credit charges.

Mitigation: Estimate costs and obtain the user's consent before paid calls, especially bulk requests.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-tiktok-product-videos)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes product-linked videos; lookups consume Qinghu credits.]

## Skill Version(s):

0.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
