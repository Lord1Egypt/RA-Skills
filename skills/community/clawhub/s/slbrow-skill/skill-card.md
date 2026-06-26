## Description: <br>
Browser automation via SLBrow MCP and HTTP API for navigating pages, analyzing content, managing tabs, searching history, extracting text, controlling the browser, and issuing curl commands through a local SLBrow server and browser extension. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adeted](https://clawhub.ai/user/adeted) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to automate browser navigation, page analysis, content extraction, tab management, history search, selected-text reading, and Seelink video AI actions through SLBrow MCP tools or REST API calls. It is intended for environments where the local SLBrow service and browser extension are installed and trusted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read browser history, selected text, and page content through the local SLBrow service. <br>
Mitigation: Use it only with trusted browser profiles and confirm explicitly before allowing history searches, selected-text reads, or page-content extraction. <br>
Risk: The skill can control browser tabs and apply Seelink video AI functions. <br>
Mitigation: Keep the SLBrow service bound to localhost, run it only when needed, and review tab-closing or video-AI actions before execution. <br>


## Reference(s): <br>
- [SLBrow REST API Reference](references/api-reference.md) <br>
- [SLBrow Workflow Checklist](SKILL_COMPACT.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/adeted/slbrow-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local SLBrow server and connected browser extension; API responses are JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
