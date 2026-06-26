## Description: <br>
Helps agents manage multiple Tailscale Serve paths for files, directories, and local ports without route conflicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snopoke](https://clawhub.ai/user/snopoke) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent for Tailscale Serve commands that expose selected local files, directories, or services at specific paths on a tailnet. It is most useful when coordinating multiple served paths and avoiding accidental root-route replacement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Serving the wrong file, directory, or port could expose sensitive local content or internal tools to the user's Tailscale network. <br>
Mitigation: Verify the exact source path or localhost port before running commands, avoid sensitive directories and unauthenticated admin tools, check tailscale serve status, and remove or reset routes when finished. <br>
Risk: Serving at the root path can override existing Tailscale Serve paths. <br>
Mitigation: Check tailscale serve status first, choose an unused subpath when adding content, and reserve tailscale serve reset for intentional replacement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snopoke/tailscale-serve) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Tailscale Serve status, serve, remove, and reset command guidance for user-selected paths, files, directories, or localhost ports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
