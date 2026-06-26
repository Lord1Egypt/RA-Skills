## Description: <br>
Wechat Workflow helps agents prepare WeChat Official Account articles, publish Markdown drafts, verify Sogou indexing, and monitor article status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luis1213899](https://clawhub.ai/user/luis1213899) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operators, and developers managing WeChat Official Accounts use this skill to turn article material into publishable Markdown drafts, configure WeChat credentials, create WeChat drafts, check Sogou visibility, and track published article status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local credential helpers can read and write WeChat secrets and may expose secret values in terminal output. <br>
Mitigation: Use a dedicated WeChat credential entry, avoid mixing unrelated secrets in the same secrets.json file, and do not run credential display commands in logged or shared terminals. <br>
Risk: Publishing workflows create WeChat drafts and make external requests to WeChat and Sogou services. <br>
Mitigation: Review article content, credentials, target account configuration, and network permissions before running publish or monitoring scripts. <br>
Risk: The publish script can globally install the wenyan npm CLI if it is missing. <br>
Mitigation: Install and review @wenyan-md/cli in advance or run the workflow in an environment where global npm installs are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luis1213899/wechat-workflow) <br>
- [Writing techniques reference](references/写作技巧.md) <br>
- [Human-style writing guide](references/去AI味指南.md) <br>
- [Popular article methodology](references/爆款方法论.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create WeChat draft content, local credential records, and article monitoring state when its scripts are executed.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
