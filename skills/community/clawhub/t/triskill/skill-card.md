## Description: <br>
Triskill gives agents three utility workflows: live fact-check lookup, bounded command failure diagnosis and retry, and local shared-memory coordination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[welove111](https://clawhub.ai/user/welove111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Triskill when an agent needs to check a factual claim against live sources, diagnose a failed shell command within a bounded retry loop, or coordinate small shared state across local agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The self-heal wrapper can capture command output in local logs, which may include sensitive data if used around secret-printing commands. <br>
Mitigation: Do not run self-heal around commands that may expose credentials or sensitive side effects; review selfheal_log.jsonl before sharing a workspace. <br>
Risk: Shared memory stores coordination data in a local unencrypted JSON file. <br>
Mitigation: Use it only for small non-secret coordination state and never store credentials, tokens, or private data. <br>
Risk: Fact-check search results can be incomplete, stale, or conflicting. <br>
Mitigation: Treat returned snippets and URLs as evidence to review, cite sources when reporting conclusions, and state uncertainty when results conflict. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/welove111/triskill) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell-command examples and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fact-check and shared-memory scripts emit JSON; self-heal records bounded command attempts in selfheal_log.jsonl.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
