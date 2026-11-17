## Description:

Publish and update agent-created HTML as private, unlisted Stacktree pages, with optional passcodes and free or paid hosting paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevysmith](https://clawhub.ai/user/stevysmith)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can turn agent-created briefs, dashboards, reports, and visualizations into shareable browser pages, then refresh them at the same link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing can share task details and page content with the hosting vendor.

Mitigation: Require explicit approval before uploading, minimize sensitive content, and use a passcode for sensitive pages.

Risk: Wallet credentials or page-management tokens can enable unauthorized page updates.

Mitigation: Prefer claim-token updates over funded-wallet access, protect management tokens, and review and pin payment dependencies before paid use.

Risk: Anonymous page content remains stored for 30 days after expiry.

Mitigation: Avoid uploading confidential content and use passcodes or expiry controls where available.

## Reference(s):

- [Stacktree homepage](https://stacktr.ee)
- [Stacktree agent documentation](https://stacktr.ee/agent.txt)
- [Stacktree authentication documentation](https://stacktr.ee/auth.md)
- [Stacktree x402 documentation](https://stacktr.ee/x402.md)
- [ClawHub release](https://clawhub.ai/stevysmith/skills/stacktree)

## Skill Output:

**Output Type(s):** [HTML, API calls, Shell commands, Guidance]

**Output Format:** [HTML pages published as private links, with HTTP requests or curl commands for publishing and updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pages can be updated at the same link; passcodes and expiry are available on supported publishing paths.]

## Skill Version(s):

1.0.8 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
