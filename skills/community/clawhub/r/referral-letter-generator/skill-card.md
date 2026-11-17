## Description:

Generate medical referral letters with patient summary, reason for referral.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare providers and clinical operations users use this skill to create structured referral letters for specialist consultation, transfer of care, urgent referral, or routine consultation from validated patient and provider data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime dependency installation can change the execution environment and may fetch packages outside the user's approved supply chain.

Mitigation: Install pinned dependencies in an isolated environment before running the skill and prevent runtime package installation.

Risk: Referral inputs and generated outputs may contain sensitive patient information.

Mitigation: Use synthetic or de-identified data unless healthcare privacy controls are in place, and keep all output paths inside an approved secure directory.

Risk: HTML output generated from untrusted referral input may be unsafe to open or share.

Mitigation: Avoid HTML output for untrusted input or sanitize and review generated HTML before viewing or distributing it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/referral-letter-generator)
- [Medical Referral Letter Generator - Quick Reference](artifact/references/quick_ref.md)
- [Input Template](artifact/references/input_template.json)
- [Medical Referral Letter Standards and Guidelines](artifact/references/referral_standards.md)
- [Medical Referral Letter Templates](artifact/references/templates.md)
- [Referral Template](artifact/references/referral_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON input templates and generated referral letter artifacts in PDF, DOCX, HTML, or TXT.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local patient/provider JSON input and writes the selected output file path.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
