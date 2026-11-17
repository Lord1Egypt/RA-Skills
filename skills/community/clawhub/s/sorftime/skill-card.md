## Description:

Sorftime helps agents generate sorftime-cli commands and scripts for Amazon, Shopee, and Walmart ecommerce data APIs, including product, keyword, category, review, subscription, and monitoring workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangfaguo](https://clawhub.ai/user/zhangfaguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and ecommerce operators use this skill to compose repeatable Sorftime CLI workflows for marketplace research, batch product and keyword lookup, review collection, and monitoring across Amazon, Shopee, and Walmart.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure through API keys, Account-SK values, active profiles, shell history, or logs.

Mitigation: Use a pinned and verified sorftime-cli release, avoid placing real keys directly in commands, prefer secured secret storage, and confirm the active profile with whoami before requests.

Risk: Remote account or marketplace-monitoring state can change through remove, delete, subscription, update, and monitoring operations.

Mitigation: Require explicit user confirmation before account removal, delete commands, subscription changes, monitoring registration, or monitoring updates.

Risk: Incorrect domain IDs, endpoint names, request payloads, or polling assumptions can produce failed requests, wasted quota, or misleading ecommerce analysis.

Mitigation: Validate domain IDs and endpoint names against the common reference, check code and message fields after each call, and include retry or polling guidance for real-time and collection endpoints.

Risk: Image-search workflows can transmit product images or derived base64 content to the remote service.

Mitigation: Confirm the user intends to submit the image, avoid sensitive or unrelated images, and explain that base64 image payloads are sent to Sorftime for processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangfaguo/skills/sorftime)
- [Sorftime CLI source repository](https://github.com/sorftime/sorftime-cli)
- [sorftime-cli npm package](https://www.npmjs.com/package/sorftime-cli)
- [Sorftime CLI account setup](https://www.sorftime.com/cli)
- [Skill quick reference](artifact/README.md)
- [Common Sorftime CLI reference](artifact/resources/_common.md)
- [Amazon monitoring reference](artifact/resources/amazon-monitoring.md)
- [Amazon workflow recipes](artifact/resources/amazon-recipes.md)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, JSON, and script examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Sorftime endpoint names, JSON request payloads, domain IDs, profile names, polling steps, and monitoring task IDs.]

## Skill Version(s):

0.1.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
