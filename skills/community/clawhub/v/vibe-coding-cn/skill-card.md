## Description: <br>
Vibe Coding Cn is an OpenClaw skill that coordinates a five-agent workflow to turn Chinese natural-language project requirements into SPEC.md, architecture, code, tests, and traceability outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gotomanutd-dot](https://clawhub.ai/user/gotomanutd-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use this skill in OpenClaw to generate or incrementally update small software projects from Chinese requirements. It produces project documentation, implementation files, tests, quality-gate feedback, version history, and traceability artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write project files and run local execution flows in the active workspace. <br>
Mitigation: Install and run it in a disposable or well-scoped workspace, and review generated diffs before using or merging the output. <br>
Risk: Optional local server and CLI modes may introduce local network and filesystem effects. <br>
Mitigation: Avoid those modes unless their behavior has been reviewed, and run them with minimal local permissions. <br>
Risk: Prompts, code, or credentials may be sent to configured LLM providers or recorded in generated logs or metadata. <br>
Mitigation: Do not provide sensitive prompts, source code, secrets, or credentials unless the configured providers and logging behavior are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gotomanutd-dot/vibe-coding-cn) <br>
- [README](artifact/README.md) <br>
- [Quickstart](artifact/QUICKSTART.md) <br>
- [OpenClaw Integration](artifact/OPENCLAW-INTEGRATION.md) <br>
- [Orchestrator Guide](artifact/ORCHESTRATOR-GUIDE.md) <br>
- [SPEC.md Format](artifact/SPEC-MD-FORMAT.md) <br>
- [Traceability Matrix](artifact/TRACEABILITY-MATRIX.md) <br>
- [Versioning Guide](artifact/VERSIONING-GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and generated project files, including SPEC.md, requirements and architecture docs, application code, tests, and optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes project output and version metadata under the configured workspace output directory.] <br>

## Skill Version(s): <br>
4.1.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
