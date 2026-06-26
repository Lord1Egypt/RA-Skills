## Description: <br>
Build reliable tool context from command output using artifacts and compact reproducible code queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmaciel](https://clawhub.ai/user/zmaciel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when command output will be analyzed by an agent and correctness, pagination handling, reproducibility, redaction discipline, or auditability matter. It guides the agent to capture output once, query artifacts with explicit root paths, and return compact answers instead of copying raw payloads into context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Captured command output can include secrets or sensitive production data. <br>
Mitigation: Avoid capturing secrets or sensitive production data, and use the skill only when queryable artifacts are appropriate for the environment. <br>
Risk: Broad artifact queries can include more context than needed for the current task. <br>
Mitigation: Prefer single-artifact scope first and widen scope only when cross-artifact analysis is required. <br>
Risk: The workflow depends on the third-party sift-gateway package and on the underlying commands selected by the user or agent. <br>
Mitigation: Install only if the package is trusted, and review underlying commands before running them. <br>


## Reference(s): <br>
- [Reliable Tool Context on ClawHub](https://clawhub.ai/zmaciel/reliable-tool-context) <br>
- [OpenClaw skill homepage](https://github.com/lourencomaciel/sift-gateway/tree/main/docs/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with shell commands and compact Python query snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance favors aggregate or top-20 query results, explicit pagination completeness checks, and avoiding raw captured payloads in model context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
