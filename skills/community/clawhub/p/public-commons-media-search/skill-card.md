## Description: <br>
Public Commons Media Search helps agents search Wikipedia and Wikimedia Commons for public media, list page media, retrieve file URLs and licensing context, and paginate Commons results through AgentPMT-hosted remote calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to discover reusable public media, retrieve Wikimedia file metadata and URLs, and check description pages for licensing context before reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote AgentPMT calls may consume credits and depend on account setup. <br>
Mitigation: Confirm the enabled AgentPMT account route and the listed 5-credit action cost before invoking the tool. <br>
Risk: Returned Wikimedia media may have file-specific license or attribution requirements. <br>
Mitigation: Verify each media item on its Wikimedia file description page before reuse. <br>
Risk: Prompts or logs could expose credentials if account details are included during setup or troubleshooting. <br>
Mitigation: Keep credentials, wallet secrets, signatures, and payment headers out of prompts and logs; use the setup guidance for credential handling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/public-commons-media-search) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/public-commons-media-search) <br>
- [Generated Action Schema](artifact/schema.md) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, JSON] <br>
**Output Format:** [Markdown instructions with JSON request examples and remote tool response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote actions return media search results, page media lists, file metadata, file URLs, pagination offsets, and licensing context.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
