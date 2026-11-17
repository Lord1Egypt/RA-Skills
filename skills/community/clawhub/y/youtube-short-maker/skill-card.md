## Description:

Make vertical YouTube Shorts with Pexo by submitting a topic or brief, then letting the hosted Pexo agent script, generate shots, add music and captions, and return the finished video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pexo](https://clawhub.ai/user/pexo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to request a short-form YouTube video from the hosted Pexo video agent, optionally including uploaded media. The agent handles project creation, file upload, status polling, user choice relay, and final asset delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts, uploaded media, project metadata, and generated assets to Pexo's hosted service.

Mitigation: Install only if you trust Pexo and have approval to share that content with the hosted service.

Risk: The skill relies on PEXO_API_KEY in ~/.pexo/config and supports PEXO_CONFIG and PEXO_BASE_URL overrides, which can expose credentials or redirect requests if misconfigured.

Mitigation: Protect ~/.pexo/config as a secret with restrictive permissions, avoid untrusted PEXO_CONFIG or PEXO_BASE_URL values, and run setup diagnostics before use.

Risk: Server security evidence flags avoidable account-security risk in credential handling and installation.

Mitigation: Review and pin the installer or source before use; deploy only after accepting the remaining risk.

## Reference(s):

- [Pexo](https://pexo.ai)
- [Setup Checklist](references/SETUP-CHECKLIST.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, project links, JSON status handling, and plain-text final asset URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PEXO_API_KEY and PEXO_BASE_URL; generated videos are produced by Pexo's hosted service and may require credits.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
