## Description: <br>
A pluggable pipe filter that strips verbose CLI output before it reaches the LLM, so an agent spends its context budget on signal instead of noise. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[workloftai](https://clawhub.ai/user/workloftai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use slim to filter large command output, logs, diffs, lockfiles, and YAML or JSON dumps before passing them into an LLM context. It helps preserve useful signal while reducing context cost for command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Filtered output can omit the middle of large command results when the lossy clamp is applied. <br>
Mitigation: Re-run the command without slim whenever exact or complete output is required. <br>
Risk: Wrapper mode executes the command provided by the user before filtering its output. <br>
Mitigation: Use wrapper mode only for commands you would already run locally; use pipe mode when you only need to filter existing output. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/workloftai/skills/slim) <br>
- [Workloft Labs](https://workloft.ai/labs) <br>
- [lowfat inspiration](https://github.com/zdk/lowfat) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; filtered command output is emitted as plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pipe mode writes filtered output to stdout; --report writes a savings summary to stderr. Large outputs may be clamped to head and tail with an elision marker.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
