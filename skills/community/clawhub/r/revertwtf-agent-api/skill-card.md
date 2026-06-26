## Description: <br>
Use revert.wtf safely from agents, tools, browsers, or integrations through bounded HTTP APIs, MCP tools, and lightweight package subpaths without downloading the full catalog into client bundles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrtdlgc](https://clawhub.ai/user/mrtdlgc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to explain EVM, RPC, provider, wallet, account-abstraction, and x402 errors, resolve selectors, search the revert.wtf catalog, and integrate bounded revert.wtf APIs or package subpaths into products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server security evidence flags high-impact moderation and GitHub workflow authority, including a review helper that may bypass sandbox approvals. <br>
Mitigation: Install only in trusted maintainer contexts, review exact commands before account, role, package, or PR changes, and prefer the autoreview helper's `--no-yolo` mode unless sandbox bypass is explicitly acceptable. <br>
Risk: The artifact handles wallet, provider, RPC, and raw error inputs where users might paste private keys, seed phrases, access tokens, unreleased exploit details, or personal data. <br>
Mitigation: Use bounded API or MCP calls and exclude private keys, seed phrases, access tokens, unreleased exploit details, and personal data from submitted inputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mrtdlgc/revertwtf-agent-api) <br>
- [revert.wtf Explain API](https://revert.wtf/api/explain) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline JSON, bash, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Promotes bounded API and MCP usage, paginated search summaries, and lightweight package subpaths.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
