## Description: <br>
Unified Self Improving gives OpenClaw agents a local memory workflow for structured learning logs, HOT/WARM/COLD storage, namespace isolation, indexing, import, recall, and repeated-pattern detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[421zuoduan](https://clawhub.ai/user/421zuoduan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to persist corrections, errors, patterns, and session notes as local memory so an OpenClaw agent can query and reuse prior learnings across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can retain sensitive prompts, credentials, customer data, or project details. <br>
Mitigation: Use the skill only when persistent local memory is intended, and avoid logging secrets or other sensitive content. <br>
Risk: File-management commands may not be safely confined to the intended memory folder. <br>
Mitigation: Use simple namespace and record names without slashes or dot-dot path segments, and prefer a patched version that validates paths before write, move, import, or delete operations. <br>
Risk: JSONL imports can add untrusted or malformed memory records. <br>
Mitigation: Import only trusted JSONL files after reviewing their contents. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/421zuoduan/unified-self-improving) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSONL/Markdown memory records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and manages local memory files under ~/.openclaw/workspace/memory when commands are used.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
