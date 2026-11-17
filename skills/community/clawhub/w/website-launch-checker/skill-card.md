## Description:

Check a small business website before go-live against a 15-point launch checklist. Use when a user asks to audit, check, review, or launch a website, or asks if a site is ready to publish. Give it a site URL, a folder of site files, or a live demo link and it returns a pass/fail report with evidence and fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmsample97](https://clawhub.ai/user/mmsample97)

### License/Terms of Use:

MIT

## Use Case:

Small business owners and website builders use this skill to review a small business site before launch. It produces an evidence-based readiness checklist and prioritized fixes from a URL, staging link, or site files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A public URL cannot establish whether the owner controls Search Console or Analytics.

Mitigation: Mark access-dependent checks for client confirmation and list the required owner step.

Risk: Submitting a live form can create a real lead or trigger follow-up.

Mitigation: Do not submit real forms without the user's permission; inspect code or form settings instead.

Risk: A launch checklist is not a comprehensive security audit.

Mitigation: Use the report as a scoped readiness check and arrange a separate security review when needed.

## Reference(s):

- [Source repository](https://github.com/mmsample97/website-launch-checker)
- [ClawHub skill release](https://clawhub.ai/mmsample97/skills/website-launch-checker)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Evidence-backed Markdown launch report with a 15-point checklist and prioritized fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports unverified checks as needing client confirmation; separates design notes from the checklist.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
