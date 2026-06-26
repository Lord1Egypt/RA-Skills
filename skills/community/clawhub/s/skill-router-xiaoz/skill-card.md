## Description: <br>
技能路由枢纽 helps OpenClaw reduce routing overhead from large skill sets by classifying tasks into scenario buckets, selecting the top relevant skills, and recording local routing outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freak30](https://clawhub.ai/user/freak30) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent builders use this skill to route task requests across many installed skills by scene, returning a small set of relevant downstream skills instead of activating the full catalog. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task snippets are saved in a local routing_log.jsonl file. <br>
Mitigation: Avoid routing secrets, credentials, sensitive business data, or personal details through the skill, and periodically review or delete the local routing log. <br>
Risk: The router may select downstream skills that can perform high-impact actions. <br>
Mitigation: Review selected downstream skills and require approval before allowing them to modify files, publish content, call external services, or use credentials. <br>
Risk: The documented learning behavior is based on simple local routing history. <br>
Mitigation: Treat selected skills as routing suggestions and verify that the chosen scene and skills fit the user request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freak30/skill-router-xiaoz) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/freak30) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with Python API examples, shell commands, and JSON-like routing results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes are based on local keyword scene buckets and recent local routing history.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
