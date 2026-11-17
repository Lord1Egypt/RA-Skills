## Description: <br>
Build reusable automation pipelines with node-to-node data flow, persisted state, error handling, and file locks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, operations staff, and automation teams use this skill to design lightweight local workflows for ETL, recurring reports, and file batch processing. It guides agents to structure reusable components, persist intermediate data and state, and prevent concurrent workflow runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Bash workflow scripts may perform filesystem writes, shell execution, and external API calls. <br>
Mitigation: Review generated run.sh files and any sourced connection files before execution. <br>
Risk: Workflow data, state, or logs may contain sensitive API responses or operational records. <br>
Mitigation: Keep credentials in environment variables or a keychain, and avoid storing sensitive responses in workflow data or logs unless intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/workflow-orchestrator-free) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Bash, JSON, and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create workflow directories, run.sh scripts, state/data/log files, and configuration files when the agent has file and shell access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
