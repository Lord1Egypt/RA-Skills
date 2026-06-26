## Description: <br>
Help automotive, small-appliance, semiconductor, and mechanical-manufacturing R&D teams solve engineering bottlenecks by finding reference cases for similar technical problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwt1995](https://clawhub.ai/user/wwt1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External R&D engineers, product developers, patent analysts, and innovation leads use this skill to find patent-derived reference cases for similar engineering tradeoffs before selecting a design direction. It is aimed at automotive, small-appliance, semiconductor, and mechanical-manufacturing problems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send sensitive engineering prompts, product designs, trade secrets, customer data, or patent strategy to an external Patsnap MCP endpoint. <br>
Mitigation: Review before installation, confirm that use of the configured Patsnap endpoint is acceptable, redact sensitive details, and consider requiring user confirmation before each search. <br>
Risk: The public MCP endpoint and APP_ID configuration may need owner approval or production authentication before release. <br>
Mitigation: Confirm that the triz-solution-search endpoint is approved for public ClawHub users and replace the test APP_ID with the approved production app id or gateway authentication method if required. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/wwt1995/solution-case-finder) <br>
- [MCP Integration](references/mcp-integration.md) <br>
- [Output Format](references/output-format.md) <br>
- [User Journey, Fallback, and Lead Capture](references/lead-and-fallback.md) <br>
- [TRIZ Query Rules](references/triz-query-rules.md) <br>
- [Example Questions](references/example-questions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured case summaries, TRIZ framing, fallback guidance, and inline configuration commands when needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [English-only responses; case retrieval uses the configured triz-solution-search MCP endpoint and should not present results as legal, infringement, freedom-to-operate, or patentability advice.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
