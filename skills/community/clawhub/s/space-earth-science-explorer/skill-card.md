## Description: <br>
Space Earth Science Explorer helps agents search NASA, NOAA, and USGS public data sources for space imagery, scientific datasets, earthquake events, and earth observation records through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, analysts, and content-focused agents use this skill to discover public space and earth science imagery, datasets, and seismic events. It is intended for science-data lookup workflows that need structured results from NASA, NOAA, and USGS sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote calls may send query text to AgentPMT and upstream public data providers and may consume the listed credits. <br>
Mitigation: Use minimal non-sensitive query text, review account and credit implications before invocation, and avoid placing secrets or private data in tool inputs. <br>
Risk: Broad activation language such as "query" could cause the skill to be selected for unrelated requests. <br>
Mitigation: Invoke it only for explicit space or earth science data tasks and confirm the action, source, time period, and limit before calling. <br>
Risk: Upstream public data sources can fail or return partial results. <br>
Mitigation: Check the returned errors array, preserve source metadata, and verify important findings against the linked result pages before relying on them. <br>


## Reference(s): <br>
- [Space Earth Science Explorer marketplace page](https://www.agentpmt.com/marketplace/space-earth-science-explorer) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/space-earth-science-explorer) <br>
- [Action schema](artifact/schema.md) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions with JSON request examples and response-field descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote AgentPMT calls return structured JSON results and may include an errors array for upstream source failures.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
