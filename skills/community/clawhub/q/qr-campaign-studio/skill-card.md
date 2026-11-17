## Description:

Generates marketing QR codes for URLs, text, WiFi, and vCards with batch output, UTM tracking links, logo embedding, poster composition, and report files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangziiiiii](https://clawhub.ai/user/wangziiiiii)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and growth operators, creators, and developers use this skill to create campaign QR assets for URLs, plain text, WiFi access, or contact cards, including batch production and poster placement. It is not intended for full short-link platforms, advanced visual design work, or payment settlement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch generation can write files based on CSV or JSON row names, which may be unsafe with untrusted batch inputs.

Mitigation: Review batch files before use, keep output directories isolated, and sanitize row names or update the script before processing untrusted inputs.

Risk: WiFi passwords and other sensitive payload data can be embedded in QR codes and reflected in generated metadata.

Mitigation: Do not place WiFi secrets or sensitive contact data in shared output directories, logs, or reports; delete metadata files when they are no longer needed.

Risk: Dependencies are version-ranged rather than pinned for reproducible production installs.

Mitigation: Pin and review dependency versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangziiiiii/skills/qr-campaign-studio)
- [Batch format reference](artifact/references/format.md)
- [Sample batch CSV](artifact/references/sample-batch.csv)
- [Jisu API](https://jisuapi.com)
- [Jisu EPC](https://jisuepc.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell command examples; generated PNG or JPEG image files and JSON metadata or report files when scripts run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate single QR assets, batch QR outputs, poster composites, and per-item metadata or batch reports from CSV or JSON inputs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
