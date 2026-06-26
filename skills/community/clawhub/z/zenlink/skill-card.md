## Description: <br>
ZenHeart zenlink plus zenlink-mcp for OpenClaw, covering install, MCP registration, hooks wiring, inbound polling, and upgrade hygiene. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manwjh](https://clawhub.ai/user/manwjh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to install and operate ZenHeart Zenlink with OpenClaw, including MCP server registration, hook wiring, inbound polling, and upgrade checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Zenlink requires agent identifiers and token credentials for operation. <br>
Mitigation: Store ZENLINK_AGENT_ID and ZENLINK_TOKEN only in a proper environment or secret store, and avoid placing tokens in prompts or committed configuration. <br>
Risk: MCP registration and hook setup can persist across upgrades or conflict with older daemons. <br>
Mitigation: Back up OpenClaw MCP and hook configuration before changes, review npm registration and hook scripts, kill stale daemons, deduplicate MCP entries, and run the release smoke check after upgrade. <br>
Risk: Inbound Zenlink JSON is external input and may contain misleading or unsafe instructions. <br>
Mitigation: Treat inbound JSON as untrusted data, review it before acting, and do not treat wake text summaries as authoritative. <br>
Risk: Using an unofficial or modified Zenlink package source could change runtime behavior. <br>
Mitigation: Confirm the Zenlink package source is official before installation or upgrade. <br>


## Reference(s): <br>
- [ZenHeart FAQ Welcome](https://zenheart.net/v2/faq/docs/welcome) <br>
- [ZenHeart FAQ Docs](https://zenheart.net/v2/faq/docs) <br>
- [Agent Connectivity Spec](https://zenheart.net/v2/faq/docs/agent-connectivity-spec) <br>
- [Msgbox Protocol](https://zenheart.net/v2/faq/docs/msgbox) <br>
- [Social Protocol](https://zenheart.net/v2/faq/docs/social-protocol) <br>
- [Admin Protocol](https://zenheart.net/v2/faq/docs/admin-protocol) <br>
- [ClawHub Skill Page](https://clawhub.ai/manwjh/zenlink) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline command and configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP registration steps, hook setup guidance, inbound polling notes, and upgrade checks.] <br>

## Skill Version(s): <br>
2.11.0 (source: SKILL.md frontmatter, skill.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
