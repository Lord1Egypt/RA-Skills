## Description:

Expose a local file, local folder, screenshot, or local HTTP service through a temporary trycloudflare.com tunnel and verify the public URL before sharing it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ojbkxiongdei](https://clawhub.ai/user/ojbkxiongdei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need to share local files, folders, screenshots, generated artifacts, or local web services through a temporary public trycloudflare.com URL. The skill emphasizes verifying the public URL before sharing it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user could unintentionally publish sensitive local files or services through a temporary public URL.

Mitigation: Use a dedicated export directory containing only the intended files, avoid home directories and project roots, and verify the exact public path before sharing.

Risk: A local administrative or sensitive localhost service could be exposed outside the machine.

Mitigation: Tunnel only known safe local services and stop the tunnel immediately after the sharing task is complete.

## Reference(s):

- [Verification Checklist](references/verification-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/ojbkxiongdei/skills/trycloudflare-proxy-verify)
- [Publisher Profile](https://clawhub.ai/user/ojbkxiongdei)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns verified temporary public URLs and operational guidance; links are temporary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
