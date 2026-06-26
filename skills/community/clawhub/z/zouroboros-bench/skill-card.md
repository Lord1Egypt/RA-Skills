## Description: <br>
Benchmark harness for AI memory systems. Evaluates LongMemEval, LoCoMo, and ConvoMem datasets against any memory backend via the zouroboros-memory CLI. Includes Mimir judge for catching architectural drift. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marlandoj](https://clawhub.ai/user/marlandoj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run repeatable memory-system benchmarks against LongMemEval, LoCoMo, and ConvoMem-style datasets, then generate reports for comparing candidate memory backends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmark conversations, memory data, or evaluation prompts may be sent to model APIs when the GPT-based judge or answer generation path is used. <br>
Mitigation: Use sanitized benchmark datasets, configure API credentials only in approved environments, and use a local model endpoint when external API transfer is not acceptable. <br>
Risk: Memory writeback behavior can affect a persistent memory database if the benchmark is pointed at a real store. <br>
Mitigation: Run benchmarks against an isolated database path via ZOUROBOROS_MEMORY_DB and avoid production memory stores unless writeback is intended. <br>
Risk: Datasets, CLI paths, and endpoint environment variables are treated as trusted inputs. <br>
Mitigation: Use trusted datasets, binaries, paths, and endpoints; review configuration before running benchmark jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marlandoj/zouroboros-bench) <br>
- [Zouroboros OpenClaw homepage](https://github.com/AlaricHQ/zouroboros-openclaw) <br>
- [Runnable local benchmark example](https://github.com/AlaricHQ/zouroboros-openclaw-examples/tree/main/examples/bench-local) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance] <br>
**Output Format:** [Markdown with inline bash commands; CLI runs can produce benchmark data and reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and benchmark/runtime environment variables for model judging and memory backend access.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
