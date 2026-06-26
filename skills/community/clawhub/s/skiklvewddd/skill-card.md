## Description: <br>
Tencent Cloud TI-ONE query toolkit for inspecting training tasks, online services, notebooks, resource groups, model repositories, datasets, logs, and events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Tencent Cloud TI-ONE operational resources through predefined read-only query scripts. It helps answer status, detail, log, event, and console-link questions without creating, modifying, or deleting cloud resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Tencent Cloud credentials and can retrieve TI-ONE operational data, including logs and service call details that may contain sensitive information. <br>
Mitigation: Use least-privilege Tencent Cloud credentials, avoid sharing transcripts that include sensitive output, and keep debug output disabled when handling or sharing results. <br>
Risk: The skill depends on local installations of tccli and jq, plus the TENCENT_TIONE_DEFAULT_REGION configuration for default region selection. <br>
Mitigation: Install the declared dependencies before use and confirm the intended region when the user has not specified one. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/skiklvewddd) <br>
- [TI-ONE tool parameter reference](references/cmd-reference.md) <br>
- [TI-ONE console reference information](references/tione-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses predefined bash scripts that call Tencent Cloud TI-ONE Describe APIs and may format results with jq.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
