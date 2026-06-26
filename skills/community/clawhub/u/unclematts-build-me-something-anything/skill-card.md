## Description: <br>
Builds one surprising, runnable local project from the user's allowed project context after collecting off-limits boundaries and optional review or tool preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uncmatteth](https://clawhub.ai/user/uncmatteth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and builders use this skill to have an agent inspect allowed local project evidence, diagnose repeated patterns, and create a fresh runnable project that moves outside the user's usual defaults. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may inspect local project or workspace files while looking for patterns. <br>
Mitigation: Set explicit off-limits paths and categories before use; avoid broad scans unless that access is intended. <br>
Risk: Generated code, commands, or configuration may be incorrect or unsuitable for a real environment. <br>
Mitigation: Keep generated files in the fresh project folder and run local proof, review, and security checks before reuse. <br>
Risk: Optional review or fix tools can introduce extra trust and installation considerations. <br>
Mitigation: Use AutoReview, ClawPatch, or missing-tool installs only when opted in, and verify tool metadata and findings before applying fixes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uncmatteth/skills/unclematts-build-me-something-anything) <br>
- [Unattended orchestration](references/unattended-orchestration.md) <br>
- [Review closeout](references/review-closeout.md) <br>
- [OpenClaw AutoReview skill](https://github.com/openclaw/agent-skills/tree/main/skills/autoreview) <br>
- [ClawPatch npm package](https://www.npmjs.com/package/clawpatch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown progress updates, project files, shell commands, and run or verification guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes are intended to stay inside a fresh project folder; optional review and fix tools are opt-in.] <br>

## Skill Version(s): <br>
7.420.70 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
