## Description: <br>
API documentation generator and diagram creator that helps agents turn OpenAPI specs, API endpoints, and code snippets into visual workflows, process diagrams, step-by-step guides, and exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[britrik](https://clawhub.ai/user/britrik) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to drive Workflow Weaver through CLI or MCP tools for API documentation, workflow diagrams, process guides, and exports from API or code inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles refresh tokens and Supabase credentials for CLI and MCP use. <br>
Mitigation: Pass credentials through documented environment variables, avoid logging secrets, and keep local config files permission-restricted. <br>
Risk: Generated diagrams and API documentation may misrepresent source APIs if inputs are incomplete or stale. <br>
Mitigation: Review generated exports against the source OpenAPI specs, endpoints, or code snippets before publishing or using them operationally. <br>
Risk: Workflow generation may require authenticated billing, quota, or BYOK setup. <br>
Mitigation: Check authentication and billing status before generation and present checkout or provider-key setup actions to the user rather than opening billing URLs automatically. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/britrik/skills/run-workflow-weaver) <br>
- [workflow-weaver npm package](https://www.npmjs.com/package/workflow-weaver) <br>
- [Workflow Weaver app](https://weaver.vibingfun.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, JSON, and configuration examples; generated Workflow Weaver exports may be Markdown, SVG, PNG, PDF, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Workflow Weaver CLI JSON output and MCP tools; generated exports depend on user-selected export format.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
