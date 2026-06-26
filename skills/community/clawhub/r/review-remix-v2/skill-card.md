## Description: <br>
Comprehensive Remix v2 code review with per-area review skills, run in parallel where the agent supports subagents and sequentially otherwise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review changed files in Remix v2 projects across routing, data flow, forms, error boundaries, SSR/performance, meta/session handling, types, and security before approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project verification commands can run npm scripts from the repository under review. <br>
Mitigation: Run npm checks only in trusted repositories or inside a container or VM. <br>


## Reference(s): <br>
- [Review Remix V2 ClawHub release](https://clawhub.ai/anderskev/review-remix-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with severity sections and verification commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review findings cite file and line evidence; post-fix verification uses npm lint, typecheck, and test commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
