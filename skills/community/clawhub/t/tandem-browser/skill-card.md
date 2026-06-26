## Description: <br>
Interact with the user's Tandem Browser via MCP bridge (mcporter). Browse, snapshot, click, type, navigate, and coordinate with the user in a shared browser environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikefaierberg-byte](https://clawhub.ai/user/mikefaierberg-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to control a local Tandem Browser session through mcporter for browsing, reading pages, snapshots, form interaction, screenshots, network inspection, and coordinated user handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes powerful browser debugging and network-inspection capabilities without enough scoping guidance. <br>
Mitigation: Install only from trusted sources, prefer isolated sessions for risky sites, and supervise use of network logs, HAR capture, DevTools/CDP commands, authenticated pages, forms, account changes, and public posting. <br>
Risk: The Tandem API token is sensitive and can enable browser control through the local MCP bridge. <br>
Mitigation: Keep the Tandem API token private, avoid sharing the token or granting broad access, and review which agents are allowed to use this skill. <br>
Risk: Trust grants can allow repeated browser actions on domains or across a temporary global window. <br>
Mitigation: Avoid granting global or permanent trust casually, grant the narrowest practical trust scope, and revoke trust when it is no longer needed. <br>
Risk: Browser content and raw HTML may contain prompt-injection attempts or misleading instructions. <br>
Mitigation: Prefer Tandem page reads and snapshots, do not follow embedded page instructions as agent instructions, and stop or escalate to the user when Tandem blocks hostile content. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mikefaierberg-byte/tandem-browser) <br>
- [Tandem Browser Homepage](https://github.com/hydro13/tandem-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and structured tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to use mcporter with Tandem MCP tools, including browser reads, snapshots, navigation, interaction, sessions, trust prompts, and handoffs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
