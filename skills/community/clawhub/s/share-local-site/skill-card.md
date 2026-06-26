## Description: <br>
Share a local development server through a public URL for demos, mobile testing, colleague review, or localhost access over the internet using ngrok, localhost.run, or cloudflared. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darwin7381](https://clawhub.ai/user/darwin7381) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to expose a local development server through a public tunnel for demos, mobile testing, pair programming, and external review before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make a local development server reachable from the public internet. <br>
Mitigation: Confirm the intended port before sharing, verify the served page, avoid exposing secrets, admin routes, debug endpoints, or private data, and stop the tunnel when sharing is finished. <br>
Risk: Some framework fixes broadly disable host protections for tunneled access. <br>
Mitigation: Prefer allowlisting the specific tunnel host when supported, and only use broad host-check bypasses for temporary development sharing. <br>
Risk: Tunnel processes can outlive the intended review window if they are run persistently. <br>
Mitigation: Track any tunnel or tmux session started for sharing and close it immediately after the demo or review is complete. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash, JavaScript, and environment variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May provide public tunnel URLs and local port checks when used by an agent.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
