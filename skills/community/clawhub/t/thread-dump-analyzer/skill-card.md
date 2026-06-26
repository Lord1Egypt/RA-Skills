## Description: <br>
Analyze thread dumps and goroutine dumps to diagnose deadlocks, thread pool exhaustion, contention hotspots, and blocked threads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose application hangs, deadlocks, blocked threads, goroutine leaks, and thread pool exhaustion across JVM, Go, Python, and Node.js runtimes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Thread and goroutine dumps can expose sensitive runtime data from live systems. <br>
Mitigation: Prefer analyzing dumps the user has already collected and sanitized, and share dump files only through approved private channels. <br>
Risk: Live dump collection commands can target the wrong process or expose pprof endpoints. <br>
Mitigation: Confirm the exact process before running collection commands and avoid exposing pprof endpoints on public networks. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/charlie-morrison/thread-dump-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and diagnostic report sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces diagnostic summaries, thread state classifications, contention hotspot analysis, root cause chains, and remediation recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
