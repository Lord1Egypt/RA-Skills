## Description:

Measures OpenClaw system response times across response stages and reports millisecond-level metrics such as TTFT, tokens per second, and total response time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingofqin2026](https://clawhub.ai/user/kingofqin2026)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to run single response-speed tests, benchmarks, and component probes for OpenClaw agents, then review timing reports to diagnose latency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Report-saving APIs can write outside the intended output folder or overwrite user-writable files when supplied an unsafe filename.

Mitigation: Keep report output under direct control, use trusted output directories and fixed filenames, and do not pass filenames from prompts, users, or external data into JSON or Markdown reporter APIs until path validation prevents traversal and unintended overwrites.

Risk: The security verdict identifies this as a suspicious beta performance-testing tool.

Mitigation: Install only where beta performance-testing tooling is acceptable and review generated reports before sharing them outside the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingofqin2026/skills/response-speed-test)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Console text, JSON, and Markdown reports with timing metrics and benchmark statistics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include staged timing points, TTFT, total response time, benchmark statistics, and optional Mermaid sequence diagrams.]

## Skill Version(s):

1.0.0 (source: release metadata, pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
