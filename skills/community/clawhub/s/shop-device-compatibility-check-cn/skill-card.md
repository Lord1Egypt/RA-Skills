## Description:

输入商家确认的设备型号、配件规格、厂家适配或排除表及顾客条件，生成逐项型号与条件对照表，标明确认适配、明确不适配或未知及资料依据。适合售前配件咨询；型号不完整、资料缺型号或仅有接口外观时，明确请求补料而不推断兼容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

供电商售前人员根据厂家适配与排除资料核对顾客询问的设备和配件组合，并给出结论、依据及仍需补充的信息。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install example uses an unpinned CLI, whose behavior may change between installs.

Mitigation: Check the package and CLI version before installation; pin versions when reproducible installs matter.

Risk: The compatibility script received only a partial security review.

Mitigation: Review the script before using it in a production workflow.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/xxjrq/skills/shop-device-compatibility-check-cn)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [逐设备—配件组合的 Markdown 对照表，列出适配状态、资料依据和待补信息；附有 JSON 示例。]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [每次最多核对 10 种设备和 10 个配件；只依据明确提供的厂家资料及条件，不代表实测或电气性能保证。]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
