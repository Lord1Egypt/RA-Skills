## Description:

Recommends open-source remote desktop alternatives to ToDesk, including RustDesk, SPyRFC, UltraVNC, and TigerVNC, with privacy-oriented setup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and IT practitioners use this skill to compare open-source remote-control tools and select privacy-oriented options for personal or self-hosted remote desktop access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The RustDesk server example uses an unpinned Docker image with host networking, which can increase exposure if copied without review.

Mitigation: Review the deployment command before use, prefer a pinned image digest, publish only required TCP/UDP ports, apply firewall restrictions, and avoid host networking unless the reduced isolation is understood and accepted.

## Reference(s):

- [RustDesk Downloads](https://rustdesk.com/download)
- [UltraVNC Downloads](https://www.uvnc.com/downloads/ultravnc.html)
- [TigerVNC](https://tigervnc.org/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with comparison tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language recommendations for remote desktop alternatives, including a RustDesk self-hosting command.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
