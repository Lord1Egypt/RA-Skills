## Description:

Searches media resources, saves Quark or Baidu share links, checks OpenList visibility and tasks, and helps copy saved resources to NAS or SMB-backed OpenList storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leochens](https://clawhub.ai/user/leochens)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search for movie, TV, animation, and other media resources, then manage the path from cloud-drive share links through OpenList verification and NAS or SMB backup copies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts can send full cloud-session cookies or OpenList tokens to unsafe caller-controlled endpoints.

Mitigation: Use only official HTTPS Quark and Baidu endpoints, use HTTPS or loopback-only OpenList, and avoid endpoint or token override flags unless the destination is fully trusted.

Risk: Save, copy, or cancellation actions can change cloud-drive or OpenList state if confirmation is skipped.

Mitigation: Keep the preview-confirm-then---yes flow for every mutating operation and review the source, selected items, destination, and final naming before execution.

Risk: Cookies and OpenList tokens in environment configuration grant account or service access.

Mitigation: Keep real secrets out of commits and logs, rely on masked readiness and cookie checks, and refresh credentials after suspected exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leochens/skills/resource-2-nas)
- [PanSou default search endpoint](https://so.252035.xyz/)
- [PanSou API endpoint](https://so.252035.xyz/api)
- [Resource 2 NAS setup guide](https://guantou.site/archives/N2CmhISt)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or JSON with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are capped to the top 50 by default; mutating save, copy, and cancellation operations are designed to use preview and explicit confirmation before execution.]

## Skill Version(s):

0.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
