## Description: <br>
安全工具执行器 classifies tools by risk tier and helps agents identify write, delete, and dangerous operations that should require approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to add tool-risk classification and approval-oriented guidance around potentially destructive commands. It is most useful as a coarse safety prompt or classifier, not as a complete enforcement layer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill claims approval and enforcement behavior, but the artifact mainly classifies tool names and returns status output. <br>
Mitigation: Use it only as coarse classification or guidance unless the publisher adds real enforcement, explicit command and path boundaries, and truthful simulation-only wording. <br>
Risk: Security evidence reports mismatched sensitive capability signals, including wallet, transaction-signing, and sensitive-credential tags. <br>
Mitigation: Review those capability tags before installation and require the publisher to remove or justify them before treating the skill as production-ready. <br>
Risk: Dangerous operations such as delete, drop, truncate, and format are security-sensitive even when routed through an approval workflow. <br>
Mitigation: Require human review for destructive operations and verify command arguments, paths, and target resources before execution. <br>


## Reference(s): <br>
- [Safe Tool Executor Skill Guide](artifact/SKILL.md) <br>
- [Safe Tool Executor Script](artifact/scripts/safe_tool_executor.py) <br>
- [ClawHub Release Page](https://clawhub.ai/kofna3369/safe-tool-executor-zh) <br>
- [Publisher Profile](https://clawhub.ai/user/kofna3369) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and command-line usage snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled Python script returns simple status and tier classification output for named tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
