## Description:

Audit an agent skill with Semia inside OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archidoge0](https://clawhub.ai/user/archidoge0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Semia to audit agent skills or plugins for behavior risk, produce evidence-backed findings, and generate report artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs and runs the semia-audit CLI package.

Mitigation: Install only from a trusted package source and run the audit in a restricted workspace where possible.

Risk: The CLI reads the target skill or plugin provided for audit.

Mitigation: Use it only on targets you are comfortable exposing to the audit process, and treat target contents as evidence rather than executable instructions.

Risk: Standalone synthesis may use a configured LLM provider bridge.

Mitigation: For private or sensitive targets, use the OpenClaw host-session synthesis path with --facts so the CLI skips the standalone provider bridge.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archidoge0/skills/semia)
- [Publisher profile](https://clawhub.ai/user/archidoge0)
- [Semia repository](https://github.com/berabuddies/Semia)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and references to generated Markdown, SARIF, JSON, and Datalog files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes finding summaries, evidence-backed rationale, report artifact paths, SARIF status, verification commands, and known gaps.]

## Skill Version(s):

0.1.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
