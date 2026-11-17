## Description:

Generate VietQR payment image URLs for Vietnamese bank transfers from bank/account details. Use when users ask to create a VietQR link, return a markdown QR preview, or validate VietQR bank/account/amount input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phucisstupid](https://clawhub.ai/user/phucisstupid)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate VietQR payment image URLs or markdown QR previews for Vietnamese bank transfers after validating bank, account, amount, note, and account-name inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bank account details, account holder names, amounts, and transfer notes can become visible in the generated third-party image URL.

Mitigation: Include only fields needed for the payment request and avoid optional personal details or sensitive transfer notes unless required.

Risk: The skill depends on the third-party img.vietqr.io image service to render the payment QR image.

Mitigation: Review the generated URL before sharing and use the skill only when that external image service is acceptable for the transfer context.

## Reference(s):

- [VietQR image service](https://img.vietqr.io/image)
- [ClawHub skill page](https://clawhub.ai/phucisstupid/skills/vietqr)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text URLs or Markdown image syntax with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated URLs may include bank account, amount, account name, and note values as query parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
