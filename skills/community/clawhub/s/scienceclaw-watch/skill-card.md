## Description: <br>
Run a live multi-agent scientific collaboration session and return a full summary when complete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fwang108](https://clawhub.ai/user/fwang108) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, scientists, and developers use this skill to run a local ScienceClaw multi-agent investigation on a scientific topic, collect competing findings, and receive a structured synthesis with generated figures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs the user's local ScienceClaw installation and depends on ANTHROPIC_API_KEY. <br>
Mitigation: Run it only in trusted workspaces with a trusted ScienceClaw install and an API key intended for this use. <br>
Risk: Workspace memory may add sensitive project context to the research topic. <br>
Mitigation: Review memory.md before execution and remove sensitive context that should not be sent to the underlying model. <br>
Risk: Generated summaries and figures remain on disk under run_exports. <br>
Mitigation: Review, retain, or delete the output directory according to the workspace's data handling needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fwang108/scienceclaw-watch) <br>
- [Publisher profile](https://clawhub.ai/user/fwang108) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown summary with file paths and JSON-backed session results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves session_summary.json and generated figures under a timestamped run_exports/watch_* directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
