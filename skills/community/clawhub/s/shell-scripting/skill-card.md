## Description: <br>
Write robust, portable shell scripts. Use when parsing arguments, handling errors properly, writing POSIX-compatible scripts, managing temp files, running commands in parallel, managing background processes, or adding --help to scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to draft, review, and improve shell scripts for automation, argument parsing, cleanup, portability, parallel execution, process management, and self-documenting command-line behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated shell commands may include destructive operations or network calls that affect real files, services, or data. <br>
Mitigation: Review scripts before running them, test on non-critical data first, and handle commands such as rm -rf, curl, and source with extra care. <br>
Risk: Parallel jobs and background processes can continue running, fail silently, or interfere with local resources if not supervised. <br>
Mitigation: Use explicit traps, waits, cleanup logic, and small test runs before applying parallel or long-running process patterns to production workflows. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated shell scripts and command examples should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
