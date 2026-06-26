## Description: <br>
QG Car helps an agent use the local qg CLI to list Qiguan campus bus schedules, choose Zhuhai, South Campus, or East Campus routes, and generate WeChat order-entry links without submitting passenger information, creating orders, or paying. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qybaihe](https://clawhub.ai/user/qybaihe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query Qiguan campus bus schedules and prepare WeChat order-entry links for supported Zhuhai, South Campus, and East Campus routes. The user completes passenger selection, order confirmation, and payment in WeChat. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help generate links that lead to ticket purchase flows. <br>
Mitigation: Keep the boundary at schedule lookup and WeChat order-entry link generation; the user must complete passenger selection, order confirmation, and payment manually. <br>
Risk: The installer replaces local skill directories and installs a global CLI. <br>
Mitigation: Inspect the installer and package source before running it, and install only when the qg-skill package or repository is trusted. <br>


## Reference(s): <br>
- [QG CLI Reference](references/qg-cli.md) <br>
- [ClawHub QG Car skill page](https://clawhub.ai/qybaihe/qgcar-skill) <br>
- [qg-skill npm package](https://www.npmjs.com/package/qg-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with CLI commands, schedule summaries, and plain copyable WeChat order-entry links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should state that generated links are order-entry links and do not represent completed bookings.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence.release.version, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
