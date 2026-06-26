## Description: <br>
AI-powered parametric furniture modeling for Fusion 360. Generates production-ready CAD models with real joinery from natural language, images, or reference links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ylzha](https://clawhub.ai/user/ylzha) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use Shopprentice to turn natural-language prompts, images, or reference links into parametric Fusion 360 furniture models with joinery. When configured with its local add-in, it can execute and iterate on generated Fusion 360 Python scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local Fusion 360 control server can inspect designs and run Fusion Python scripts without authentication. <br>
Mitigation: Install only when the publisher is trusted, enable MCP only when live Fusion execution is needed, stop the add-in when not in use, and review generated scripts before execution. <br>
Risk: Generated scripts can alter active CAD work if run in the wrong document mode. <br>
Mitigation: Capture document state before execution, use additive mode for untracked user work, and reserve clean rebuilds for models the agent intentionally owns. <br>
Risk: The one-line installer fetches and runs a remote shell script that changes local client and Fusion 360 configuration. <br>
Mitigation: Review the installer source, prefer explicit installer flags for the clients in use, and skip MCP setup unless local CAD execution is required. <br>


## Reference(s): <br>
- [Shopprentice ClawHub page](https://clawhub.ai/ylzha/shopprentice) <br>
- [Shopprentice homepage](https://github.com/ShopPrentice/shopprentice) <br>
- [Installer source](https://github.com/ShopPrentice/shopprentice/blob/main/install.sh) <br>
- [README](README.md) <br>
- [Fusion 360 API Rules](docs/fusion-api-rules.md) <br>
- [MCP Advanced](docs/mcp-advanced.md) <br>
- [Joinery Reference](docs/joinery/README.md) <br>
- [Hardware Installation](docs/hardware-installation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Fusion 360 Python scripts and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a local MCP add-in to execute generated Fusion 360 scripts and inspect CAD documents when configured.] <br>

## Skill Version(s): <br>
0.7.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
