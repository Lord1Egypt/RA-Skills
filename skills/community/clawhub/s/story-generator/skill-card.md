## Description: <br>
This skill helps an agent generate multi-episode story scripts with graph-backed continuity, AI quality review, and human confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hexidyg](https://clawhub.ai/user/hexidyg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators and developers use this skill to run a structured episode-generation workflow for short-form story or video scripts, including continuity prompts, review prompts, state tracking, and approval checkpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Graph storage can read, write, or delete local JSON files too broadly if a crafted pipeline ID is supplied. <br>
Mitigation: Review before installing, use only non-sensitive story content, avoid path-like pipeline IDs, and prefer a release that validates pipeline IDs and confines graph files to the skill data directory. <br>
Risk: Deletion and state-changing operations may affect stored story graph data without a clear recovery path. <br>
Mitigation: Back up generated story state before use and require explicit confirmation before deleting or ending pipelines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hexidyg/story-generator) <br>
- [Publisher profile](https://clawhub.ai/user/hexidyg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-compatible workflow responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces generation prompts, review prompts, pipeline status objects, and local story graph/state files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
