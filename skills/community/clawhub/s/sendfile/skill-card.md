## Description: <br>
Send files to users in chat by creating a temporary public download link via aitun tunnel. Perfect for AI agents that need to deliver generated files (documents, images, reports, code) to users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ctz168](https://clawhub.ai/user/ctz168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to deliver generated local files to users by exposing a temporary browser-accessible download link. It is most useful when direct chat upload is unavailable, too large, or otherwise unsuitable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a local directory through a public tunnel. <br>
Mitigation: Share only non-sensitive files from a dedicated temporary directory containing the exact file intended for download. <br>
Risk: Remote one-line installer examples can execute unreviewed code. <br>
Mitigation: Prefer the pip or uv installation path described in the server guidance. <br>
Risk: Temporary servers and tunnels may remain active longer than needed. <br>
Mitigation: Start the tunnel only after the user requests a download link, then stop both the HTTP server and tunnel immediately after transfer. <br>


## Reference(s): <br>
- [AiTun homepage](https://aitun.cc) <br>
- [ClawHub skill page](https://clawhub.ai/ctz168/skills/sendfile) <br>
- [ClawHub package link](https://clawhub.ai/ctz168/sendfile) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and a temporary download URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces temporary public links for user download; avoid sensitive files.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
