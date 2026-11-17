## Description:

Benchmark harness for AI memory systems. Evaluates LongMemEval, LoCoMo, and ConvoMem datasets against any memory backend via the zouroboros-memory CLI. Includes Mimir judge for catching architectural drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marlandoj](https://clawhub.ai/user/marlandoj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run repeatable memory-system benchmarks, compare LongMemEval, LoCoMo, and ConvoMem-style results, and generate reports for candidate memory backends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted benchmark inputs can reach shell-command execution paths.

Mitigation: Use trusted datasets, run the skill in an isolated workspace, and review generated commands before running them against shared systems.

Risk: Benchmark conversation context can be sent to external model services when OpenAI-backed judging or answering is enabled.

Mitigation: Use local-only model settings for sensitive data, or run with a restricted account and datasets cleared for external processing.

Risk: Mimir writeback can persist changes into application memory state.

Mitigation: Use an isolated benchmark database and keep rollback or disposable test data when evaluating non-production memory systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marlandoj/skills/zouroboros-bench)
- [OpenClaw homepage](https://github.com/AlaricHQ/zouroboros-openclaw)
- [Runnable starter example](https://github.com/AlaricHQ/zouroboros-openclaw-examples/tree/main/examples/bench-local)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Benchmark runs may generate local run data and reports through the package CLI.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
