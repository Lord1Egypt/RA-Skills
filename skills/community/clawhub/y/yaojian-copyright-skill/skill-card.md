## Description:

Yaojian Copyright Registration & Evidence helps agents guide creators through DCI confirmation, blockchain evidence preservation, copyright certificate workflows, and infringement-response questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alanqin888](https://clawhub.ai/user/alanqin888)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and external users use this skill to preserve evidence for original works, request Yaojian account actions, submit micro-chain evidence orders, obtain certificate images, and ask copyright, DCI, fee, legal-effect, and infringement-response questions grounded in the Yaojian knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill authenticates to a Yaojian account and stores tokens, mobile login context, and identity-owner records locally.

Mitigation: Use a dedicated account where possible, restrict workspace access, and clear local token and credential caches after completing the workflow.

Risk: The workflow may read and upload original works and identity-related records for evidence preservation.

Mitigation: Use it only when the user is comfortable with Yaojian processing the selected files and identity-owner data, and avoid highly sensitive unpublished works unless that handling is acceptable.

Risk: Payment QR data can be exposed when converting order payment URLs through a third-party QR service.

Mitigation: Review the order details before payment and avoid sharing payment QR links or generated QR images outside the active payment session.

Risk: Certificate image filenames are derived from work titles.

Mitigation: Use sanitized titles and review generated certificate paths before opening, storing, or sharing certificate images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alanqin888/skills/yaojian-copyright-skill)
- [Yaojian knowledge base](https://oss.fuyaoshuzhi.com/assets/yaojian/%E7%88%BB%E9%89%B4%E9%97%AE%E9%A2%98%E5%BA%93.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and concise text with inline shell commands and generated certificate image references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce payment QR-code links, order status summaries, and certificate image paths during guided evidence-preservation workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
