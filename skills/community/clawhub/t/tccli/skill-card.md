## Description: <br>
Provides a Tencent Cloud CLI reference for installing, configuring, and using TCCLI commands across common Tencent Cloud services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sxhoio](https://clawhub.ai/user/sxhoio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill as a quick reference for Tencent Cloud CLI setup, command lookup, output formatting, and common operations on services such as CVM, Lighthouse, VPC, SSL, DNSPod, and monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tencent Cloud credentials or secret values can be exposed through shared terminals, logs, screenshots, or repositories. <br>
Mitigation: Use least-privilege credentials and avoid displaying or committing secretId, secretKey, account details, and command output containing sensitive values. <br>
Risk: Write commands can change live Tencent Cloud resources, including instances, DNS records, certificates, firewall rules, and networking configuration. <br>
Mitigation: Verify the target account, region, resource IDs, domains, DNS values, certificate IDs, and command intent before executing write operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sxhoio/tccli) <br>
- [TCCLI official documentation](https://cloud.tencent.com/document/product/440/34011) <br>
- [TencentCloud CLI GitHub repository](https://github.com/TencentCloud/tencentcloud-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with command examples and reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may affect live Tencent Cloud resources when users run them outside the agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
