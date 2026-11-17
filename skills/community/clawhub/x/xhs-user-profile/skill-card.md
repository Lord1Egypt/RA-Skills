## Description:

Collects public Xiaohongshu creator profile posts and exports post details for content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuiyunhai](https://clawhub.ai/user/cuiyunhai)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing analysts and creator partnership teams use this skill to review a public Xiaohongshu creator's posts, assess content, and export note listings for research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default service address uses unencrypted HTTP, exposing account tokens in transit.

Mitigation: Use a verified HTTPS service address before logging in, if available.

Risk: Disabling TLS certificate verification can expose account sessions to interception.

Mitigation: Do not enable insecure TLS; use a service with a valid certificate.

Risk: Collection and session steps consume paid credits.

Mitigation: Explain the charge and obtain user confirmation before each paid action.

Risk: Stored tokens, automatically imported legacy credentials, and exported CSV files contain sensitive information.

Mitigation: Check whether legacy credential import is wanted, protect saved tokens and exports, and avoid sharing them publicly.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cuiyunhai/skills/xhs-profile)

## Skill Output:

**Output Type(s):** [JSON, CSV files, Shell commands, Guidance]

**Output Format:** [JSON command results and optional CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include collected post details and billing totals; CSV exports are available on request.]

## Skill Version(s):

2.0.1 (source: frontmatter, package.json, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
