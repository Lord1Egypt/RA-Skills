## Description:

Converts batches of public Xiaohongshu note links, including short links, into browser-ready links with xsec_token through a paid service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuiyunhai](https://clawhub.ai/user/cuiyunhai)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents converting public Xiaohongshu note links use this skill to obtain viewable links, optionally for subsequent engagement-data collection with xhs-dpt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default plaintext HTTP service can expose tokens, submitted links and task data in transit.

Mitigation: Use a trusted HTTPS service with valid certificates before logging in or submitting links; keep insecure mode disabled.

Risk: A reusable local token is shared with xhs-dpt and can be exposed by an untrusted service URL or unsafe handling.

Mitigation: Protect the local credential file, do not share tokens, and avoid untrusted base URLs.

Risk: Converting valid links spends credits, and some unsuccessful conversions are not refunded.

Mitigation: Check the balance and batch contents before submitting; inspect per-link results and refund amounts afterward.

## Reference(s):

- [小红书转链 on ClawHub](https://clawhub.ai/cuiyunhai/skills/xhs-convert-url-pro)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON task results and plain-text converted links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Converted links include xsec_token; results may include per-link status, failure reasons and credit charges.]

## Skill Version(s):

2.0.1 (source: frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
