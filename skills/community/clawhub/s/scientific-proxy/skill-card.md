## Description: <br>
Scientific Proxy helps an agent fetch, test, and format free public proxy nodes for OpenClaw users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtmpss](https://clawhub.ai/user/mtmpss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to obtain tested public proxy configurations and device-specific setup guidance for common proxy clients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Free public proxy nodes are untrusted and may observe or tamper with traffic. <br>
Mitigation: Use the generated proxies only for low-sensitivity activity and avoid banking, email, work accounts, financial activity, or other sensitive browsing. <br>
Risk: The skill downloads mutable public proxy lists and tests remote endpoints from local Python code. <br>
Mitigation: Install and run it only when that network behavior is intended, and review the local cache and generated configuration before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mtmpss/scientific-proxy) <br>
- [Shadowrocket AI](https://shadowrocket.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-like conversational text with proxy configuration snippets and setup steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated from tested public proxy nodes when available and may include Clash, V2Ray, Shadowrocket/Base64, or text formats.] <br>

## Skill Version(s): <br>
1.8.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
