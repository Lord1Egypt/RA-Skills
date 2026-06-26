## Description: <br>
SlowMist Agent Security is a security review framework for AI agents covering skill and MCP installation, repositories, URLs and documents, on-chain interactions, products and services, and social shares. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[slowmist](https://clawhub.ai/user/slowmist) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and agent operators use this skill to route external inputs through structured security checks and produce standardized risk reports before installation, execution, wallet interaction, or service adoption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional external risk tools may receive sensitive addresses, URLs, or artifacts during review. <br>
Mitigation: Send only the specific item needed for the assessment, and never share private keys, seed phrases, or unrelated personal context. <br>
Risk: The conservative review posture can slow or block high-risk actions, including wallet or credential-related workflows. <br>
Mitigation: Use the generated report as a decision aid and require explicit human approval before proceeding with high-risk or rejected actions. <br>
Risk: Markdown reports and guidance may be mistaken for final proof of safety. <br>
Mitigation: Verify source identity, inspect relevant artifacts, and treat the report as one input to a broader security decision. <br>


## Reference(s): <br>
- [SlowMist Agent Security on ClawHub](https://clawhub.ai/slowmist/slowmist-agent-security) <br>
- [SlowMist ClawHub Publisher Profile](https://clawhub.ai/user/slowmist) <br>
- [Project Homepage](https://github.com/slowmist/slowmist-agent-security) <br>
- [OpenClaw Security Practice Guide](https://github.com/slowmist/openclaw-security-practice-guide) <br>
- [SlowMist](https://slowmist.com) <br>
- [skill-vetter inspiration](https://clawhub.ai/spclaudehome/skill-vetter) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Text] <br>
**Output Format:** [Structured Markdown security assessment reports and review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses standardized report templates and a conservative four-level risk rating model.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
