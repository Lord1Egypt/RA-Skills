## Description: <br>
Use UniFuncs Deep Research API to run in-depth research and generate long-form reports of 10,000 words or more when users request deep research, research reports, or comprehensive analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vinlic](https://clawhub.ai/user/vinlic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit confirmed research topics to UniFuncs Deep Research, then receive long-form reports or query asynchronous research task results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default synchronous report flow can start a detached background process that continues using the UniFuncs API key and writing output after the visible command returns. <br>
Mitigation: Require explicit user confirmation before running, prefer the async create/query scripts when the user needs clearer control, and monitor or read the stream file before considering the run complete. <br>
Risk: Research prompts and generated report content are sent to UniFuncs and stream files may contain sensitive output. <br>
Mitigation: Avoid confidential data unless UniFuncs is approved for the use case, confirm the exact topic and options before execution, and delete stream files that may contain sensitive report output. <br>
Risk: Deep research can be long-running and higher cost than ordinary search. <br>
Mitigation: Confirm the expected runtime, cost posture, model, output type, and topic with the user before invoking any script. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/vinlic/unifuncs-deep-research) <br>
- [UniFuncs Account and API Key Setup](https://unifuncs.com/account) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text reports, JSON task/status payloads, and shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Long-running report generation can stream partial content to a local stream file; the default output length hint is 10000 words.] <br>

## Skill Version(s): <br>
0.0.7 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
