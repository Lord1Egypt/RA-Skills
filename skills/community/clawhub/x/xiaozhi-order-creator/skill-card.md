## Description:

Create Xiaozhi Recycle orders for devices or clothing through Bearhome APIs, with optional device-nameplate OCR to prefill device details before user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiongdong-tech](https://clawhub.ai/user/xiongdong-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to help users collect pickup, contact, device, clothing, and timing details, confirm the order summary or OCR-derived fields, request WeChat authorization, and submit Xiaozhi recycling orders.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill sends personal contact, pickup address, order details, and optional device photos or image URLs to Xiaozhi/Bearhome services.

Mitigation: Use it only when the user is comfortable sharing those details with the service, and show the order summary before authorization.

Risk: The documented flow submits the order automatically after WeChat authorization.

Mitigation: Confirm the final order summary, OCR-derived fields, and clothing price before asking the user to scan the authorization code.

Risk: Temporary QR code image or HTML authorization files may remain on shared machines.

Mitigation: Remove temporary QR and HTML files after use, especially on shared systems.

Risk: OCR-derived brand, category, and model values are inferred and may be inaccurate.

Mitigation: Display OCR results to the user and allow correction before using them in an order.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xiongdong-tech/skills/xiaozhi-order-creator)
- [Xiaozhi Recycle API Reference](artifact/references/api.md)
- [Bearhome OCR Nameplate Reference](artifact/references/ocr.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary QR code image or local HTML authorization files and submit recycling orders after user authorization.]

## Skill Version(s):

0.1.2 (source: server release metadata; artifact frontmatter lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
