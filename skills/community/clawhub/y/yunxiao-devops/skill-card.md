## Description: <br>
Yunxiao DevOps helps agents interact with Alibaba Cloud Yunxiao DevOps across project collaboration, Codeup repositories, Flow pipelines, AppStack delivery, package, testing, insight, and knowledge workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codingadai](https://clawhub.ai/user/codingadai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps teams use this skill to inspect and operate Yunxiao projects, work items, merge requests, pipelines, releases, and application delivery flows from an agent. It supports routine DevOps workflows by producing command guidance, helper-script invocations, API-call examples, and configuration instructions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports hardcoded account details and an embedded Yunxiao token. <br>
Mitigation: Remove or rotate embedded credentials and require explicit user configuration through environment variables or local config files before use. <br>
Risk: The security evidence reports powerful repository-changing automation for bug-fix, release, pipeline, and merge-request flows. <br>
Mitigation: Use least-privilege tokens, repository allowlists, and confirmation gates before enabling flows that can push code, merge changes, tag releases, or trigger production pipelines. <br>
Risk: The security guidance calls for stop controls for background pollers. <br>
Mitigation: Run pollers under explicit supervision with logging, timeouts, and a documented stop procedure. <br>


## Reference(s): <br>
- [Projex Guide](references/projex-guide.md) <br>
- [Pipeline YAML Guide](references/pipeline-yaml-guide.md) <br>
- [Pipeline YAML Syntax](references/pipeline-yaml-syntax.md) <br>
- [Workflow Transitions](references/workflow-transitions.json) <br>
- [Yunxiao OpenAPI Docs Index](references/api-docs/INDEX.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, API-call snippets, JSON payloads, and script invocations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call local Node.js and Python helper scripts that interact with Yunxiao and Feishu services when configured.] <br>

## Skill Version(s): <br>
2.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
