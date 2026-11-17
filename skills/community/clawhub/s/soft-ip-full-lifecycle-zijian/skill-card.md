## Description:

Software IP self-assessment skill that delivers Chinese software copyright application compliance review after clawtip payment verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinyu12166](https://clawhub.ai/user/jinyu12166)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, software teams, and applicants preparing Chinese software copyright registration use this skill to check material completeness, source-code documentation, user manuals, rights attribution, and registration readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local order files may persist the user's question and payment metadata.

Mitigation: Avoid submitting source code, applicant identity details, trade secrets, or complete legal materials in the question, and remove local order files when they are no longer needed.

Risk: Payment verification is weak if local credential fields are trusted without signed credential validation.

Mitigation: Verify the clawtip tooling provenance and require signed credential validation before relying on payment status for sensitive or high-value use.

Risk: The service produces compliance guidance that may affect software copyright filings.

Mitigation: Treat the output as self-assessment guidance and have qualified legal or IP reviewers check filing decisions before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinyu12166/skills/soft-ip-full-lifecycle-zijian)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown guidance with shell command output and JSON_RESULT status lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires clawtip payment verification before the AI-delivered compliance review proceeds.]

## Skill Version(s):

3.1.44 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
