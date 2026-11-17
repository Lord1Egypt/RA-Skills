## Description:

Extracts departure station, destination station, train number, seat, fare, travel date, ID number, and ticket sales details from train ticket images using the Sugon-Scnet OCR service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to send train ticket images or PDFs to the Sugon-Scnet OCR API and receive structured ticket fields for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticket images and PDFs can contain personal data and are uploaded to Scnet's external OCR service.

Mitigation: Use the skill only with appropriate authorization, limit inputs to intended train ticket files, and review the destination service before production use.

Risk: The skill accepts a local file path and can upload any readable file to a configurable API base URL.

Mitigation: Validate file paths before execution, keep SCNET_API_BASE at the trusted default unless explicitly verified, and avoid passing arbitrary local paths.

Risk: The SCNET_API_KEY credential is required for use.

Mitigation: Store the API key in an environment variable or protected local configuration file, keep file permissions restrictive, and do not paste the key into chat.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scnet-sugon/skills/train-ticket-ocr)
- [Sugon-Scnet OCR API Summary](artifact/references/api-docs.md)
- [Train Ticket Field Summary](artifact/assets/templates/fields-summary.md)
- [Scnet Website](https://www.scnet.cn)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON, guidance]

**Output Format:** [JSON data on standard output, with text error messages for configuration, network, API, and rate-limit failures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCNET_API_KEY and accepts TRAIN_TICKET plus a local file path as command-line inputs.]

## Skill Version(s):

1.0.3 (source: frontmatter, skill.yaml, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
