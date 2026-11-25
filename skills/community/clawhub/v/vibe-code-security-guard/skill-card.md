## Description:

Scans deployed apps built with AI coding tools for exposed secrets, source maps, publicly readable Supabase tables, and missing security headers, then provides a grade and fix prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memeanalyst](https://clawhub.ai/user/memeanalyst)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to check a deployed app they own or have permission to test before launch, after fixes, or when they want to review its exposed public surface. It reports findings with an A–F grade and remediation prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A benign scan verdict may be incomplete because a referenced state file was unavailable during review.

Mitigation: Review the unresolved reference and treat the scan as a point-in-time exposure check, not a guarantee of safety.

Risk: Scanning a site without permission could test a system the user is not authorized to assess.

Mitigation: Scan only sites the user owns or has written permission to test; request explicit ownership confirmation before owner-mode Supabase checks.

Risk: Scans incur a per-site charge on the user's Apify account.

Mitigation: Tell the user the $0.05 per-site cost before the first scan and use the user's own Apify token.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/memeanalyst/skills/vibe-code-security-guard)
- [Vibe Code Security Scanner on Apify](https://apify.com/magnova/vibe-code-security-scanner)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown security report with an A–F grade, findings, and fix prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Point-in-time checks of the deployed app's public surface; reports findings without printing full secrets. Each site scan costs $0.05 on the user's Apify account.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
