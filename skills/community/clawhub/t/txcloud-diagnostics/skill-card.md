## Description: <br>
用于腾讯云云产品异常诊断。当用户反馈腾讯云相关的任何异常、产品/实例不可用等情况时，根据反馈的实例和异常信息，自动拉取监控等数据进行分析诊断，输出原因和建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crueluncle](https://clawhub.ai/user/crueluncle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operators, support engineers, and developers use this skill to diagnose Tencent Cloud product or instance issues by collecting monitoring data, checking product-specific metrics, and producing a concise diagnosis with recommended actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate Tencent Cloud authentication and handle authorization artifacts in /tmp. <br>
Mitigation: Use a least-privilege Tencent Cloud account, protect shared-machine access, and clean up temporary authorization files and logs after use. <br>
Risk: The skill can run remote TAT shell commands on Tencent Cloud instances. <br>
Mitigation: Review the target instance, metric scope, and every TAT command before execution; keep remote commands read-only and avoid broad administrative credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/crueluncle/txcloud-diagnostics) <br>
- [Tencent Cloud product documentation](https://cloud.tencent.com/document/product) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown diagnosis report with tables and concise action recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request Tencent Cloud authorization and may use tccli commands to gather monitoring data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
