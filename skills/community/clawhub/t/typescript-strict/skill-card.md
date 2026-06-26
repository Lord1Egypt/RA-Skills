## Description: <br>
Guides agents through incremental TypeScript strictness adoption, including compiler flags, typing boundaries, narrowing, generics, utility types, CI guardrails, and safe refactors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawkk](https://clawhub.ai/user/clawkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to plan and execute incremental TypeScript strict-mode migrations, reduce unsafe any usage, harden IO boundaries, and keep type-safety regressions out of CI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proposed TypeScript configuration, CI gates, or large refactors can change build behavior or block releases. <br>
Mitigation: Review proposed tsconfig, CI, and refactor changes before applying them; roll them out incrementally and run type checks and tests before merge. <br>
Risk: Guidance can be less accurate if the agent assumes the wrong TypeScript version, build tool, or monorepo layout. <br>
Mitigation: Confirm the TypeScript version, build tool, and package layout before planning strictness changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawkk/typescript-strict) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, Code] <br>
**Output Format:** [Markdown with inline TypeScript, configuration, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose TypeScript compiler flags, validation patterns, CI guardrails, and incremental refactor steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
