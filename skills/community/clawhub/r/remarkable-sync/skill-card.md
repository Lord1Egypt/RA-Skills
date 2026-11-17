## Description:

Bidirectional sync with reMarkable tablet via Cloud API (rmapi). Fetch handwritten notes/sketches, process with AI, and push content back. Use for sketch enhancement, journal extraction, or sending documents/images to the tablet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolmanns](https://clawhub.ai/user/coolmanns)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to fetch handwritten notes, sketches, and documents from a reMarkable tablet, process them locally or with AI tools, and upload supported PDF or EPUB content back to the tablet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install mutable third-party tools and Python packages used in a tablet sync workflow.

Mitigation: Verify or pin the rmapi binary and Python packages before use, and install them in a dedicated environment where practical.

Risk: The workflow stores a persistent reMarkable cloud token and may process sensitive handwritten notes or sketches.

Mitigation: Protect ~/.rmapi as a credential file and sync only notebooks or documents suitable for local tooling and any downstream AI services involved.

## Reference(s):

- [ClawHub skill release: reMarkable Tablet Sync](https://clawhub.ai/coolmanns/skills/remarkable-sync)
- [rmapi releases](https://github.com/ddvk/rmapi/releases)
- [reMarkable desktop connection page](https://my.remarkable.com/connect/desktop)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown guidance with shell commands and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides use of rmapi, rmc, CairoSVG, and Pillow; does not include executable bundled code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
