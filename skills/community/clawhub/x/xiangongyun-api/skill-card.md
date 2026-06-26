## Description: <br>
仙宫云GPU云服务平台API集成工具，支持实例管理、私有镜像管理、账号管理等全量操作；当用户需要查询或管理仙宫云GPU实例、操作私有镜像、查询账户余额或充值时使用 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chsengni](https://clawhub.ai/user/chsengni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to query and manage Xiangongyun GPU cloud instances, private images, account balance, and recharge orders through the Xiangongyun open API. It is intended for authenticated account administration where instance lifecycle, image deletion, and billing actions are reviewed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent direct destructive and billing-related controls over a Xiangongyun GPU cloud account. <br>
Mitigation: Require explicit user confirmation that includes the exact target ID, action, cost or data-loss impact before deploy, destroy, release-GPU, save-and-destroy, image deletion, or recharge commands. <br>
Risk: The API token enables account administration if exposed or over-privileged. <br>
Mitigation: Use the least-privileged Xiangongyun token available and keep config/config.yaml private. <br>
Risk: Asynchronous lifecycle actions may return before the requested operation has actually completed. <br>
Mitigation: After deployment, shutdown, destroy, or image operations, query the instance or image status before taking dependent actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chsengni/xiangongyun-api) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/chsengni) <br>
- [Xiangongyun API Reference](references/api_reference.md) <br>
- [Xiangongyun API Endpoint](https://api.xiangongyun.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses from the Xiangongyun API script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Xiangongyun API access token in config/config.yaml and sends authenticated GET and POST requests to the configured Xiangongyun API base URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
