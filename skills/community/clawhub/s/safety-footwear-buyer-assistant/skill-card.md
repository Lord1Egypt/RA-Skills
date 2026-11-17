## Description:

The skill helps B2B PPE buyers match safety footwear products, compare material and certification tradeoffs, prepare RFQs, verify suppliers, and draft local simulated inquiries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fly0pants](https://clawhub.ai/user/fly0pants)

### License/Terms of Use:

MIT-0

## Use Case:

External PPE buyers, importers, distributors, sourcing teams, industrial purchasers, and workwear brands use this skill to evaluate PVC boots, EVA boots, rubber boots, and safety shoes; compare application fit and certification needs; prepare supplier questions; and create simulated inquiry drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents as a general buyer assistant while its examples, product references, and live follow-up path are centered on one supplier.

Mitigation: Treat product matches and linked resources as supplier-specific references, compare against independent supplier evidence, and verify certifications, MOQ, lead time, and live contact channels before procurement decisions.

Risk: The simulated inquiry flow accepts buyer contact details locally, which could be mistaken for a live supplier submission.

Mitigation: Do not enter real buyer contact details unless using the local simulation intentionally, and separately choose where to send any real inquiry.

## Reference(s):

- [Safety Footwear RFQ Template](references/rfq-template.md)
- [Supplier Verification Checklist](references/supplier-verification.md)
- [ClawHub skill page](https://clawhub.ai/fly0pants/skills/safety-footwear-buyer-assistant)
- [Reliable Safety Products](https://reliablesafetyboots.com)
- [PVC vs EVA vs Rubber work boots guide](https://reliablesafetyboots.com/blog/pvc-vs-eva-vs-rubber-boots)
- [Supplier verification guide](https://reliablesafetyboots.com/supplier-verification)
- [Safety footwear certification evidence guide](https://reliablesafetyboots.com/blog/safety-boot-certification-buyer-guide)
- [Safety footwear quality inspection checklist](https://reliablesafetyboots.com/blog/safety-footwear-quality-inspection-checklist)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product search uses bundled static data; inquiry submission is a local simulation that does not transmit or persist buyer data.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
