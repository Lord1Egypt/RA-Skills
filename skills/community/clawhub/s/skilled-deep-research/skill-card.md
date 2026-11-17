## Description:

Researches a topic across web, GitHub, Reddit, government, academic, and other sources to produce cited reports, ranging from quick inline summaries to checkpointed parallel research runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanford](https://clawhub.ai/user/seanford)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agent operators use this skill to gather multi-source evidence and produce cited research reports. It supports quick inline research as well as standard or deep workflows with parallel workers, checkpointed progress, deduplication, retries, and final Markdown report synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad auto-triggered research workflows can initiate multi-agent browsing and file-writing activity unexpectedly.

Mitigation: Review before installing, narrow activation where possible, and run only in a constrained workspace.

Risk: Persistent local logs, progress files, retry queues, and reports may contain sensitive research topics, URLs, or findings.

Mitigation: Avoid sensitive research topics unless persistent local logs are acceptable, restrict workspace access, and remove run data after use when appropriate.

Risk: Unvalidated slugs, worker names, URLs, or output paths may create unsafe shell or file-write behavior.

Mitigation: Use trusted inputs, avoid arbitrary output paths, and validate paths, URLs, slugs, and worker names before running the skill.

Risk: External tools required by the workflow may change behavior across environments.

Mitigation: Pin and review documented external tools before deployment, including mcporter, Playwright MCP, and search or fetch helpers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/seanford/skills/skilled-deep-research)
- [OpenClaw](https://openclaw.ai)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [Declared Project Homepage](https://github.com/seanford/skilled-deep-research)
- [ddg-search](https://github.com/seanford/ddg-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, cited summaries, command snippets, status text, and JSON progress metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write checkpoint, progress, retry queue, and final report files under the OpenClaw skills-data workspace, with an optional user-specified report copy path.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
