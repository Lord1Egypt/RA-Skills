## Description: <br>
Generates HTML product-promotion email templates by extracting product images and details from ecommerce URLs, saving reusable marketing assets, and optionally sending the email through SMTP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szzg007](https://clawhub.ai/user/szzg007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce operators, marketers, and developers can use this skill to turn a product URL into reusable promotional email assets, including downloaded product images, an HTML email template, metadata, and a report. It can also support direct email sending when SMTP credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports embedded SMTP credentials and weakened TLS protections in the bundled email sender. <br>
Mitigation: Remove bundled credentials, rotate any exposed credential, require user-provided scoped SMTP credentials, and restore normal TLS certificate verification before use. <br>
Risk: The skill can send outbound marketing email. <br>
Mitigation: Preview generated content and confirm the recipient, subject, sender identity, and applicable marketing-email consent or compliance requirements before every send. <br>
Risk: The skill downloads and reuses product images from ecommerce pages. <br>
Mitigation: Verify rights to use each downloaded image and product claim before publishing or sending generated promotional materials. <br>


## Reference(s): <br>
- [Skill README](README.md) <br>
- [Usage Examples](references/USAGE_EXAMPLES.md) <br>
- [Email Code System](references/CODE_SYSTEM.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/szzg007/szzg007-product-promotion) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown status summaries plus generated HTML email templates, image files, JSON metadata, and shell-command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download product images, write marketing assets to a local library, and send outbound email when SMTP settings are supplied.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact documentation and package metadata report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
