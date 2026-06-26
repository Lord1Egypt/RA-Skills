## Description: <br>
Zero-to-Launch helps independent developers and founders turn rough product ideas into a structured launch plan covering users, competitors, market sizing, validation, MVP scope, and prototype sketches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viliawang-pm](https://clawhub.ai/user/viliawang-pm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, founders, makers, and product managers use this skill to clarify a product intuition, explore the market and user assumptions, and define a validation path before launch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release package includes unrelated WeChat publishing tools with account credentials and write access to a third-party platform. <br>
Mitigation: Remove or clearly separate the WeChat publisher from the planning skill before normal installation, and review any publishing commands before execution. <br>
Risk: The security guidance reports an exposed WeChat secret and checked-in config.json secrets. <br>
Mitigation: Delete checked-in secrets, rotate affected WeChat credentials, and keep local publishing configuration outside the released package. <br>
Risk: The artifact mixes a product-planning coach identity with WeChat publishing assets. <br>
Mitigation: Align documentation, metadata, and packaged files to one skill identity before release. <br>


## Reference(s): <br>
- [ClawHub Zero-to-Launch page](https://clawhub.ai/viliawang-pm/zero-to-launch) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Example conversations](artifact/examples/CONVERSATIONS.md) <br>
- [WeChat publisher README](artifact/wechat-publisher/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown conversation with structured planning artifacts, tables, and ASCII sketches] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request web search for competitive analysis when the host agent supports it.] <br>

## Skill Version(s): <br>
3.0.6 (source: server release metadata; artifact frontmatter reports 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
