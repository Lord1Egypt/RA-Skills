## Description: <br>
Executes multi-step workflows through Orchestrate for complex, parallel, multi-model automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JPaulGrayson](https://clawhub.ai/user/JPaulGrayson) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to run YAML-defined workflows through Orchestrate for web search, LLM analysis, synthesis, and social posting tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow YAML files may be uploaded to an external service for execution. <br>
Mitigation: Review every workflow before running it, keep secrets out of workflow files, and use --dry before execution. <br>
Risk: Workflows may trigger actions in connected services, including public posting. <br>
Mitigation: Add a manual approval step before workflows post publicly or change external accounts. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/JPaulGrayson/quack-workflow) <br>
- [Orchestrate platform](https://orchestrate.us.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and YAML workflow configuration; workflow execution returns JSON from Orchestrate.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send local workflow YAML contents to orchestrate.us.com unless --dry is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
