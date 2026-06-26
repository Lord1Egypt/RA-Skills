## Description: <br>
Use the connected scholar-sidekick-mcp MCP server when the user mentions a scholarly identifier and wants structured metadata, a formatted citation, a bibliography export file, a retraction check, an open-access check, or verification that a claimed citation is real. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mlava](https://clawhub.ai/user/mlava) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, librarians, editors, and developer agents use this skill to resolve scholarly identifiers, format citations, export bibliography records, check retraction or open-access status, and verify whether a claimed citation matches a real record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Citation identifiers or pasted citation details may be sent to the external Scholar Sidekick service. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and avoid confidential manuscripts or private reference lists unless approved. <br>
Risk: The skill requires a RAPIDAPI_KEY for the connected MCP server. <br>
Mitigation: Configure the key only in the MCP server environment and avoid exposing it in prompts, shared logs, or generated outputs. <br>
Risk: If the MCP server is unavailable, citation, retraction, open-access, and verification answers may not have authoritative lookup data. <br>
Mitigation: Stop and report that the Scholar Sidekick MCP tools are unavailable instead of fabricating fallback answers. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mlava/scholar-sidekick-mcp) <br>
- [Scholar Sidekick homepage](https://scholar-sidekick.com) <br>
- [Scholar Sidekick RapidAPI listing](https://rapidapi.com/scholar-sidekick-scholar-sidekick-api/api/scholar-sidekick) <br>
- [Citation Style Language styles](https://github.com/citation-style-language/styles) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with citation strings, structured metadata summaries, and bibliography export content when the connected MCP tools return it] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected scholar-sidekick-mcp MCP server with RAPIDAPI_KEY for live citation, verification, retraction, and open-access lookups.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
