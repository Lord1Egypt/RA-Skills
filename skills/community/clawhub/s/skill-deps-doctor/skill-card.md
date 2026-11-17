## Description:

Cross-platform skill dependency doctor — preflight check for missing binaries, version mismatches, system libraries, CJK fonts, Playwright/Chromium runtime, and project-level deps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rangeking](https://clawhub.ai/user/rangeking)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to preflight agent skill and project runtime dependencies before execution, generate fix guidance or scripts, and produce CI-readable dependency reports for regression gating.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback wrapper can import executable Python code from the current working directory.

Mitigation: Use the normal installed skill-deps-doctor command or a vendored trusted package, and avoid the fallback wrapper from untrusted project directories.

Risk: The main package installation is unpinned, which can change the installed code over time.

Mitigation: Install from a trusted, pinned release when possible before using the skill in CI or production-like workflows.

## Reference(s):

- [Skill Deps Doctor on ClawHub](https://clawhub.ai/rangeking/skills/skill-deps-doctor)
- [rangeking publisher profile](https://clawhub.ai/user/rangeking)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown or text reports, JSON for CI, and shell fix scripts when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also produce environment snapshots, dependency graphs, platform matrices, and baseline regression gate results depending on command options.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
