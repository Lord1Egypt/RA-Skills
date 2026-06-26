## Description: <br>
Analyzes TypeScript and TSX API code by keyword, function name, or API path, then produces structured Markdown documentation for request methods, paths, parameters, responses, and status codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[9talk](https://clawhub.ai/user/9talk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to inspect TypeScript API implementations and generate concise Markdown tables describing endpoints, request parameters, response structures, comments, and code snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated documentation can expose API paths, type structures, comments, and code snippets from inspected repositories. <br>
Mitigation: Use the skill only on repositories whose API details can appear in assistant conversation output, or redact sensitive code before analysis. <br>
Risk: When source code lacks explicit documentation, the skill may include inferred methods or status codes. <br>
Mitigation: Review generated Markdown before publishing or relying on it as API reference material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/9talk/ts-interface-miner) <br>
- [Publisher profile](https://clawhub.ai/user/9talk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown tables with optional TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include inferred status codes or method details when source code does not state them explicitly.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
