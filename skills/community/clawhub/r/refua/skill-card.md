## Description: <br>
Refua helps agents fold and score biomolecular complexes and optionally profile ADMET to prioritize molecules in drug discovery workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jbenjoseph](https://clawhub.ai/user/jbenjoseph) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Drug discovery researchers and computational chemistry operators use this skill to run Refua workflows through refua-mcp for complex folding, affinity scoring, design workflows, and optional ADMET profiling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the local Refua MCP server and installing related Python packages can introduce package-source and environment trust risk. <br>
Mitigation: Install only in a trusted, isolated Python environment and verify the refua and refua-mcp package sources before running the server. <br>
Risk: Confidential molecular structures may be exposed through local server behavior, logs, caches, or downloaded assets. <br>
Mitigation: Avoid confidential molecular structures unless the installed packages and local storage behavior are trusted and understood. <br>


## Reference(s): <br>
- [Refua on ClawHub](https://clawhub.ai/jbenjoseph/refua) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with shell commands and MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on the local refua-mcp server, installed Refua extras, model assets, and user-provided molecular inputs.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
