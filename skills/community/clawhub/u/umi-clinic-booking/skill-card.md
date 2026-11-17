## Description:

Umi helps users view booking information, submit appointment requests, consult customer service, check prices, and access app download links for UMI Skin Clinic in Myeongdong, Seoul.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beautsgo](https://clawhub.ai/user/beautsgo)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get UMI Skin Clinic booking guidance, submit appointment requests through BeautsGO, consult customer service, and check treatment prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privacy-sensitive booking details may be sent to BeautsGO during the booking flow.

Mitigation: Require explicit user confirmation immediately before submission and show the destination service and fields being sent.

Risk: The package contains hard-coded API tokens.

Mitigation: Move tokens to managed secrets or configuration, rotate exposed tokens, and avoid shipping credentials in the skill artifact.

Risk: Browser opening uses shell execution for URLs.

Mitigation: Replace shell execution with a safer URL-opening library or platform API and keep strict HTTPS host allowlisting.

Risk: The Android APK link is not verified by the evidence.

Mitigation: Prefer official app-store links and clearly label any direct APK download as requiring publisher verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beautsgo/skills/umi-clinic-booking)
- [BeautsGO UMI Skin Clinic booking page](https://i.beautsgo.com/cn/hospital/umi-skin-clinic/skill)
- [BeautsGO UMI Skin Clinic detail page](https://i.beautsgo.com/cn/hospital/umi-skin-clinic?from=skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-formatted string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include user-facing links, booking submission status, price results, or clinic guidance.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, skill.json, package.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
