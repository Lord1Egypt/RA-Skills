## Description: <br>
一个用于闲鱼虚拟商品自动发货的代理技能，通过浏览器自动监控聊天、识别付款系统卡片，并按配置发送秘钥、链接、图片、文件或调用自定义发货流程。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sliverp](https://clawhub.ai/user/sliverp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External sellers and developers use this skill to automate delivery of virtual goods on Xianyu after payment confirmation. It is intended for configurable fulfillment workflows such as key-pool delivery, download-link delivery, file delivery, image delivery, API-based delivery, and custom scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform unattended actions through a logged-in Xianyu marketplace account. <br>
Mitigation: Use a dedicated browser profile and test account first, and add human confirmation or dry-run behavior before enabling live auto-delivery. <br>
Risk: Fulfillment keys or other virtual-goods secrets may be stored or logged in plaintext. <br>
Mitigation: Avoid storing real keys in plaintext where possible, restrict access to key files and logs, and remove sensitive values from logs before sharing them. <br>
Risk: Custom fulfillment scripts, external APIs, or notification templates can send data to endpoints controlled outside the skill. <br>
Mitigation: Review any my-fulfillment.sh script before running it and disable API or notification templates unless the endpoint is trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sliverp/xianyu-auto-saler) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact quick start](artifact/QUICKSTART.md) <br>
- [Goofish Xianyu IM](https://www.goofish.com/im) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash scripts and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses agent-browser and a logged-in browser profile; fulfillment behavior depends on user-provided templates and configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
