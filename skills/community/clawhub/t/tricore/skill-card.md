## Description: <br>
TriCore is a deterministic three-layer memory and cognitive framework for OpenClaw agents, with a Python memory controller, policy constraints, and planning, ReAct, and self-evolution skill templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bertonhan](https://clawhub.ai/user/bertonhan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use TriCore to install a workspace-level memory framework that routes planning state, session notes, and knowledge base entries through memctl.py instead of scattered files. It is intended for OpenClaw environments that support memory_search and memory_get. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install script modifies workspace policy and OpenClaw compaction configuration. <br>
Mitigation: Review the POLICY.md diff and compaction prompt change before installation, and install first in a test workspace or with backups. <br>
Risk: The installer may migrate an oversized MEMORY.md into memory/archive and replace it with a minimal template. <br>
Mitigation: Back up the workspace before installation and review any archived legacy memory file before redistributing content into the new memory structure. <br>
Risk: The bundled self-evolution skill can guide web-informed code and configuration changes. <br>
Mitigation: Disable or remove self-evolution unless runtime code modification is explicitly desired and reviewed. <br>


## Reference(s): <br>
- [TriCore ClawHub release](https://clawhub.ai/bertonhan/tricore) <br>
- [Publisher profile](https://clawhub.ai/user/bertonhan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash and Python command examples plus installable script and skill files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workspace memory files, policy configuration changes, and cognitive skill templates when installed.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
