## Description: <br>
Python debugging assistant that helps diagnose and fix Python code errors, including common exceptions such as SyntaxError, TypeError, and NameError. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laninga](https://clawhub.ai/user/laninga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze Python tracebacks, inspect code snippets, identify likely root causes, and receive concise repair guidance with debugging tips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debugging prompts may include secrets, private tokens, or proprietary code. <br>
Mitigation: Review and redact sensitive values before sharing code, tracebacks, configuration, or environment details with the agent. <br>
Risk: The skill may respond in Chinese by default because the artifact instructions and examples are written in Chinese. <br>
Mitigation: Ask the assistant to respond in the user's preferred language when needed. <br>
Risk: Suggested fixes can be incorrect or incomplete for code not fully represented in the prompt. <br>
Mitigation: Review proposed changes, run tests, and execute repaired code in a controlled environment before relying on the result. <br>


## Reference(s): <br>
- [Python Built-in Exceptions](https://docs.python.org/3/library/exceptions.html) <br>
- [Python Common Errors Quick Reference](references/common-errors.md) <br>
- [Python Debugging Tools Guide](references/debugging-tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown diagnostic report with code blocks and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces error analysis, code-location notes, repair steps, corrected Python code, and targeted debugging suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
