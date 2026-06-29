## Description: <br>
Text Manipulation and Converter helps agents manipulate, convert, clean, normalize, sort, deduplicate, wrap, quote, and count text through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill to perform text cleanup, case conversion, line operations, quoting, wrapping, and character or word counts with the AgentPMT text manipulation service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted text is processed by the remote AgentPMT service and may include sensitive content if users paste it into tool calls. <br>
Mitigation: Avoid sending secrets, regulated data, private code, customer data, or confidential text unless AgentPMT processing is acceptable. <br>
Risk: Generic cleanup requests could trigger remote calls that consume credits. <br>
Mitigation: Use explicit invocation and review intended AgentPMT actions before running paid remote text-processing calls. <br>


## Reference(s): <br>
- [Text Manipulation And Converter on ClawHub](https://clawhub.ai/agentpmt/skills/text-manipulation-and-converter) <br>
- [Text Manipulation And Converter Marketplace](https://www.agentpmt.com/marketplace/text-manipulation-and-converter) <br>
- [Generated Action Schema](artifact/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown instructions with JSON request examples and text or JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include transformed text, counts, action metadata, and live schema guidance for AgentPMT calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
