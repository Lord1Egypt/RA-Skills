## Description: <br>
ZMT Browser Matrix Manager - Control multi-account browser matrix via HTTP API <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wociaozhongyunonghaole](https://clawhub.ai/user/wociaozhongyunonghaole) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and automation operators use this skill to list, start, stop, and query accounts in a local ZMT multi-account browser matrix through its HTTP API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external matrix tool and local HTTP API may manage browser profiles, cookies, account sessions, and IP or proxy settings. <br>
Mitigation: Install and use the skill only when you intend to control that local ZMT setup, and review the external tool and local API separately before operational use. <br>
Risk: Natural-language or scripted account controls could start, stop, or query the wrong browser account if account names are ambiguous. <br>
Mitigation: Confirm target account names and intended actions before sending commands to the local API. <br>


## Reference(s): <br>
- [ZMT Matrix Tool](https://zmt.scys6688.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include natural-language instructions for controlling local account browser sessions.] <br>

## Skill Version(s): <br>
1.0.16 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
