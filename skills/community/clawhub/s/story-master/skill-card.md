## Description: <br>
Story Master helps agents generate multi-episode scripts through a persistent story pipeline with graph-managed characters, scenes, hooks, AI review, and human confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hexidyg](https://clawhub.ai/user/hexidyg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators and developers use this skill to plan, generate, review, pause, resume, and complete serialized scripts. It supports multi-episode story continuity by tracking prior episodes, characters, scenes, hooks, review results, and user confirmation state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted pipeline ID can cause graph file operations outside the intended graph storage folder. <br>
Mitigation: Review before installing, avoid manually supplied arbitrary pipeline IDs, and use a fixed version that validates pipeline IDs and confines graph paths under data/graphs. <br>
Risk: Story material and pipeline state may be persisted locally, and graph operations may use the documented remote endpoint. <br>
Mitigation: Use non-sensitive story material unless local persistence and the configured endpoint are acceptable for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hexidyg/story-master) <br>
- [Graph interface endpoint documented by the skill](https://framedream.art/n8n/webhook-test/open_frame_construct) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-like status objects with Python API call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes generated episode content, review prompts, pipeline status, and graph-backed story context.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
