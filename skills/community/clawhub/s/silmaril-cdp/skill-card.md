## Description: <br>
Browser automation, DOM inspection, page mutation, wait orchestration, flow execution, and local proxy override work through the Silmaril Chrome DevTools Protocol toolkit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Malac12](https://clawhub.ai/user/Malac12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect and automate Chrome pages through CDP, extract structured page data, orchestrate waits, run repeatable browser flows, and manage local proxy overrides when page response mutation is required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: JavaScript evaluation and page mutation commands can change live page state or execute untrusted code in the browser session. <br>
Mitigation: Validate selectors and intent before mutation, require explicit action flags, and use unsafe JavaScript only in trusted local sessions. <br>
Risk: Proxy override workflows can intercept or alter web responses during local browsing. <br>
Mitigation: Use narrow URL matching, keep proxy listeners on loopback, require explicit MITM acknowledgement, and keep overrides temporary unless persistence is requested. <br>
Risk: Installing a missing external toolkit introduces remote code into the user's environment. <br>
Mitigation: Fetch or install the toolkit only after the user explicitly approves that action. <br>


## Reference(s): <br>
- [Command Patterns](references/command-patterns.md) <br>
- [Flow Runner](references/flows.md) <br>
- [Proxy Workflow](references/proxy.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Malac12/silmaril-cdp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, text] <br>
**Output Format:** [Markdown with inline PowerShell commands, JSON command examples, and concise procedural guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to request explicit approval before fetching or installing remote toolkit code.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
