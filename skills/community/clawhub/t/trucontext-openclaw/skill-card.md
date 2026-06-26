## Description: <br>
TruContext OpenClaw gives OpenClaw agents a wrapper for TruContext persistent memory, including recall, graph queries, gap checks, health checks, and entity-node operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alphacollectivellc](https://clawhub.ai/user/alphacollectivellc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agents use this skill to remember significant context across sessions, recall relevant prior work, query a TruContext knowledge graph, inspect gaps and health signals, and manage entity nodes through the tc-memory wrapper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory operations may store or recall sensitive, private, or wrong-workspace context. <br>
Mitigation: Use only in workspaces where TruContext is trusted, avoid secrets and private client data, and verify the active workspace and root before recall or ingest. <br>
Risk: Wrapper behavior can fall back to the first configured agent when the current workspace does not match a registered workspace. <br>
Mitigation: Prefer a version that fails closed on workspace mismatch, and confirm configuration in ~/.trucontext/openclaw-state.json before using memory commands. <br>
Risk: Shell and Python wrapper handling may pass local paths or arguments unsafely in edge cases. <br>
Mitigation: Review wrapper commands before deployment and prefer a version that safely passes paths and arguments to Python and the TruContext CLI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alphacollectivellc/trucontext-openclaw) <br>
- [TruContext homepage](https://trucontext.ai) <br>
- [trucontext-openclaw npm package](https://www.npmjs.com/package/trucontext-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use the tc-memory wrapper and depend on local TruContext CLI configuration and authentication.] <br>

## Skill Version(s): <br>
0.1.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
