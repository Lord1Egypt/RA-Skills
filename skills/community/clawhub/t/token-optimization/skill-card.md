## Description: <br>
Reduce OpenClaw per-turn prompt costs by 70%+ through file splitting, prompt caching, context pruning, and model routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jack-Yang-ai](https://clawhub.ai/user/Jack-Yang-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit OpenClaw prompt usage and apply file-splitting, prompt caching, context pruning, and model-routing changes that reduce per-turn token costs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace file edits and OpenClaw configuration changes can alter future agent behavior or remove useful context. <br>
Mitigation: Inspect and back up BOOTSTRAP.md, AGENTS.md, MEMORY.md, and openclaw.json before applying the guide. <br>
Risk: Prompt caching, pruning, and heartbeat settings can change context retention, cache behavior, or background activity. <br>
Mitigation: Apply only settings you are comfortable with, then monitor session status, cache hit rate, context usage, and compactions after restart. <br>


## Reference(s): <br>
- [OpenClaw Prompt Caching docs](https://docs.openclaw.ai/reference/prompt-caching) <br>
- [Session Pruning docs](https://docs.openclaw.ai/concepts/session-pruning) <br>
- [Gateway Configuration](https://docs.openclaw.ai/gateway/configuration) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell and JSON configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes user-directed OpenClaw workspace and gateway configuration changes.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
