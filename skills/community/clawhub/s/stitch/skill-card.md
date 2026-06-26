## Description: <br>
Guides agents through using Google Stitch's remote MCP server to manage projects and screens and generate or edit UI designs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arielletolome](https://clawhub.ai/user/arielletolome) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Designers, developers, and agents use this skill to connect to an authenticated Google Stitch workspace, inspect or create projects, retrieve screen assets, and generate or edit UI screens through remote MCP calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mutating Stitch actions can create or change remote projects and screens in an authenticated workspace. <br>
Mitigation: Confirm the target project or screen before running mutating tools, and use test projects for experiments. <br>
Risk: Screen generation and editing can continue after connection errors, which may lead to duplicate remote changes if retried immediately. <br>
Mitigation: Do not retry generation or editing blindly; wait and inspect progress with the relevant screen retrieval call. <br>
Risk: The skill relies on a Google Stitch API key for remote access. <br>
Mitigation: Provide the key through environment or client configuration, avoid embedding it in shared files, and rotate it if exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/arielletolome/stitch) <br>
- [Google Stitch MCP Setup and Authentication](https://stitch.withgoogle.com/docs/mcp/setup/) <br>
- [Google Stitch MCP Reference](https://stitch.withgoogle.com/docs/mcp/reference/) <br>
- [Google Stitch MCP Guide](https://stitch.withgoogle.com/docs/mcp/guide/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON, bash, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes remote MCP tool names, request arguments, authentication setup, and workflow guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
