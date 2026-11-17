## Description:

Helps create and manage email marketing campaigns, subscriber lists, reusable templates, and basic campaign reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinanping-cpu](https://clawhub.ai/user/yinanping-cpu)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to draft email marketing workflows, maintain CSV subscriber lists, create campaign configuration files, and run local campaign send simulations or sends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles subscriber data and can store or print customer information in local CSV, JSON, and stdout outputs.

Mitigation: Use test lists unless consent and compliance controls are in place, and protect or delete generated subscriber files and logs after review.

Risk: Campaign, list, and template names have weak boundaries and may affect which local files are read or written.

Mitigation: Use only trusted names, run from a dedicated working directory, and inspect generated campaign files before sending.

Risk: Local send status and analytics may be misleading and should not be treated as proof that messages were delivered or engaged with.

Mitigation: Validate delivery and analytics with the real email service provider or SMTP system before using results for business decisions.

Risk: Real marketing sends can create consent, unsubscribe, and anti-spam compliance obligations.

Mitigation: Confirm recipient consent, unsubscribe handling, sender identity, and applicable CAN-SPAM, GDPR, or local requirements before using real customer data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinanping-cpu/skills/yinan-email-marketing)
- [Taobao seller workbench](https://myseller.taobao.com/home.htm/QnworkbenchHome/)
- [Douyin shop homepage](https://fxg.jinritemai.com/ffa/mshop/homepage/index?channel=zhaoshang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash examples and local JSON, CSV, and text file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local campaign JSON files and CSV subscriber lists; stdout logs may include subscriber addresses and send status.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
