## Description: <br>
Stack Exchange API integration with managed OAuth for Q&A knowledge automation across Stack Exchange sites. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to search Stack Exchange sites, retrieve Q&A content, inspect tags and user activity, and work with authenticated account data through ClawLink OAuth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth-backed tools can access private account-adjacent data such as inbox items, notifications, achievements, and token metadata. <br>
Mitigation: Install only if the user trusts ClawLink with the Stack Exchange OAuth connection, and require explicit user intent before invoking authenticated or private-account tools. <br>
Risk: Automated use of token-inspection or private-account tools may expose sensitive account information in agent context or logs. <br>
Mitigation: Avoid token and private-account tool calls unless needed for the user's request, and review returned data before sharing or storing it. <br>


## Reference(s): <br>
- [Stack Exchange API Documentation](https://api.stackexchange.com/docs) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=stack-exchange) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawHub Stack Exchange Skill](https://clawhub.ai/hith3sh/stack-exchange) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON tool arguments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Stack Exchange API result summaries and OAuth-backed account data when tools are invoked.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
