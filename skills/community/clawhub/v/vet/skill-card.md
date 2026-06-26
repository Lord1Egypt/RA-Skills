## Description: <br>
Run vet immediately after ANY logical unit of code changes. Do not batch your changes, do not wait to be asked to run vet, make sure you are proactive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrewlaack-collab](https://clawhub.ai/user/andrewlaack-collab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and coding agents use vet after small units of code change to review git diffs and, when enabled, conversation history for implementation issues or request mismatches. It is intended to supplement, not replace, normal test runs and human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: History-backed review can expose local coding-agent transcripts, tool output, secrets, or proprietary details to vet. <br>
Mitigation: Use no-history mode for sensitive work, verify the exact session file or session ID before running, and only enable history-backed runs when users have opted into that data flow. <br>
Risk: The security review flags the release for review because the skill proactively reads local session histories. <br>
Mitigation: Prefer pinned or isolated installation and review the generated command before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andrewlaack-collab/vet) <br>
- [vet repository](https://github.com/imbue-ai/vet) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, shell commands] <br>
**Output Format:** [Markdown with inline shell commands and review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run with or without conversation-history export scripts for Codex, Claude Code, and OpenCode.] <br>

## Skill Version(s): <br>
0.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
