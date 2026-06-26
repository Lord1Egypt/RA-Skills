## Description: <br>
Create fallback site adapters for websites that do not expose native WebMCP. Use when a site needs a new adapter module, tool schema design, browser-side request execution, or request-template extraction from observed page behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create or update fallback WebMCP site adapters when a website lacks native WebMCP support. It guides adapter scaffolding, tool contract design, browser-side request execution, request-template extraction, fallback behavior, and test coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scaffold helper can run unintended local code if given crafted adapter details. <br>
Mitigation: Review or patch the scaffold script before use, and do not pass untrusted site names, hosts, URLs, display names, or package names to it. <br>
Risk: Generated adapters may perform authenticated site actions through the user's browser session. <br>
Mitigation: Confirm generated adapters only perform the authenticated site actions intended by the user, and keep credential replay or auth bypass logic out of the adapter. <br>


## Reference(s): <br>
- [End-to-end adapter creation flow](references/workflow.md) <br>
- [Network discovery](references/network-discovery.md) <br>
- [Request template patterns](references/request-template-patterns.md) <br>
- [Adapter runtime patterns](references/adapter-runtime-patterns.md) <br>
- [Testing expectations](references/testing.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, code, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to scaffold adapter files and validate generated adapter behavior.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
