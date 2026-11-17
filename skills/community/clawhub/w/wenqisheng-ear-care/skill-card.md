## Description:

Provides AI customer-service guidance for Wenqisheng Ear Care store inquiries, including locations, hours, appointments, services, promotions, Wi-Fi, brand information, and ear and eye care FAQ.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liubuq-sys](https://clawhub.ai/user/liubuq-sys)

### License/Terms of Use:

MIT-0

## Use Case:

External customers use this skill through an agent or supported messaging bot to get store-specific answers about Wenqisheng Ear Care locations, hours, services, promotions, appointments, and safety-sensitive ear or eye care questions. Store operators can maintain the reference files that ground those customer-service responses.

### Deployment Geography for Use:

China (Nanchang, Jiangxi store operations)

## Known Risks and Mitigations:

Risk: Automatic installation and daily updates of mutable remote code can change deployed behavior without review.

Mitigation: Remove auto-install and auto-update persistence, and install only pinned, verified releases.

Risk: Pipe-to-shell installation can execute remote installer changes before a user reviews them.

Mitigation: Replace pipe-to-shell installation with a downloaded, checksum-verified release artifact and a documented manual install path.

Risk: Public bot deployment without complete webhook authentication and rate limits can expose customer-service endpoints to abuse.

Mitigation: Add real webhook signature verification, platform-specific secrets, request validation, and rate limits before public deployment.

Risk: Urgent ear or eye symptom guidance could delay qualified medical care.

Mitigation: Change urgent symptom responses to direct users to qualified medical care first, and keep store evaluation guidance secondary.

Risk: Unrelated development-bot roles in the bot server broaden the release beyond the storefront customer-service use case.

Mitigation: Delete or separate unrelated bot-server roles from the customer-service skill release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liubuq-sys/skills/wenqisheng-ear-care)
- [Business info reference](references/business-info.md)
- [Services reference](references/services.md)
- [Promotions reference](references/promotions.md)
- [FAQ reference](references/faq.md)
- [Brand reference](references/brand.md)
- [Bot server guide](bot-server/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Natural-language text or Markdown, with optional shell commands and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are intended to be grounded in the reference files; store data should be read at query time.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
