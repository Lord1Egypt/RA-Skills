## Description: <br>
Tool lifecycle UI components for React/Next.js from ui.inference.sh that help display tool calls, status, approvals, results, and errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building React/Next.js agent interfaces use this skill to add UI components for tool-call status, progress, human approval, successful results, and error states. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote install commands can change project files or pull newer component code than expected. <br>
Mitigation: Review the referenced registry source before execution, pin versions where practical, and run setup only in projects intended for modification. <br>
Risk: Tool approval UI can be miswired so sensitive actions execute without the intended human confirmation. <br>
Mitigation: Verify approval and denial callbacks during integration tests before using the components in agent workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/okaris/tools-ui) <br>
- [ui.inference.sh tool components](https://ui.inference.sh/blocks/tools) <br>
- [Tool component registry JSON](https://ui.inference.sh/r/tools.json) <br>
- [Adding Tools to Agents](https://inference.sh/docs/agents/adding-tools) <br>
- [Human-in-the-Loop](https://inference.sh/docs/runtime/human-in-the-loop) <br>
- [Tool Approval Gates](https://inference.sh/blog/tools/approval-gates) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and TSX code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference remote shadcn and npx commands that modify a React/Next.js project.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
