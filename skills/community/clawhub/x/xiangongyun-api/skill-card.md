## Description:

仙宫云GPU云服务平台API集成工具，支持实例管理、私有镜像管理、账号管理等全量操作；当用户需要查询或管理仙宫云GPU实例、操作私有镜像、查询账户余额或充值时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[chsengni](https://clawhub.ai/user/chsengni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to query and manage Xiangongyun GPU cloud instances, private images, account balance, and recharge orders through the Xiangongyun open API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform destructive Xiangongyun cloud actions such as instance destruction, shutdown-and-destroy, image destruction, GPU release, and save-and-destroy.

Mitigation: Require manual confirmation before destructive or GPU-release actions, and verify target instance or image IDs before execution.

Risk: The skill can initiate billing-related actions, including deployment and recharge-order creation.

Mitigation: Require manual confirmation before deployment or recharge-order actions, and confirm amount, payment method, and expected cloud costs.

Risk: The skill handles Xiangongyun API credentials and may accept sensitive access details such as passwords or private keys.

Mitigation: Use a least-privilege token when available, keep tokens outside shared or version-controlled directories, and avoid passing passwords or private keys on the command line.

Risk: The skill sends authenticated requests to a configurable API base URL.

Mitigation: Verify the API base URL before use and keep it set to the expected Xiangongyun API endpoint unless intentionally changed.

## Reference(s):

- [Xiangongyun API Reference](references/api_reference.md)
- [Xiangongyun API Base URL](https://api.xiangongyun.com)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, JSON, Configuration]

**Output Format:** [JSON responses from a Python command-line API client, with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Xiangongyun API access token and requests>=2.28.0.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
