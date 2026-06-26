## Description: <br>
Legacy ClawHub listing for Qoris Memory that directs users to install the canonical qoris-memory-mcp skill while preserving backward compatibility for existing qoris-memory users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apps-debug](https://clawhub.ai/user/apps-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this legacy listing to identify the migrated Qoris Memory skill and configure an MCP-backed memory service with QORIS_API_KEY and QORIS_WORKSPACE_ID when continuing to use the old slug. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory content and knowledge documents are sent to and stored by the Qoris MCP service for the configured workspace. <br>
Mitigation: Use the skill only for data appropriate for that workspace and avoid storing secrets, regulated data, customer records, or confidential prompts unless access controls, retention, deletion, and key rotation have been verified. <br>
Risk: The skill requires sensitive credentials through QORIS_API_KEY and QORIS_WORKSPACE_ID. <br>
Mitigation: Provide credentials through environment variables or an approved secrets manager, rotate keys when needed, and do not commit credential values to source control. <br>
Risk: This is a legacy listing that no longer receives future feature updates. <br>
Mitigation: Install and review the canonical qoris-memory-mcp listing for new deployments unless backward compatibility with the qoris-memory slug is specifically required. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/apps-debug/qoris-memory) <br>
- [Canonical qoris-memory-mcp listing](https://clawhub.ai/qoris-memory-mcp) <br>
- [Qoris homepage](https://qoris.ai) <br>
- [Qoris Memory documentation](https://docs.qoris.ai/memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses explicit MCP memory tools and requires QORIS_API_KEY and QORIS_WORKSPACE_ID.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence, frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
