## Description: <br>
AI-powered code review for Q/kdb+ that helps catch correctness, performance, and security issues in finance-oriented Q code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beee003](https://clawhub.ai/user/beee003) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Quant developers, kdb+ DBAs, and trading infrastructure teams use this skill to review Q/kdb+ files for bugs, type and rank errors, performance pitfalls, and security vulnerabilities. It supports standard, strict, and security-focused review modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reviewed Q/kdb+ code and configured provider API keys may be sent to Astrai and downstream model providers. <br>
Mitigation: Use separate or limited-scope API keys, unset provider keys that should not be routed, monitor provider billing, and avoid submitting confidential trading logic or embedded secrets unless the data flow is approved. <br>
Risk: Review findings and suggested Q code may be incomplete or incorrect. <br>
Mitigation: Have a qualified Q/kdb+ reviewer validate findings and test any suggested code changes before relying on them in trading or production systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/beee003/q-kdb-code-review) <br>
- [beee003 publisher profile](https://clawhub.ai/user/beee003) <br>
- [Astrai service](https://as-trai.com) <br>
- [Astrai chat completions endpoint](https://as-trai.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, guidance, configuration] <br>
**Output Format:** [Markdown-style review summary with severity labels, file and line references, explanations, and suggested Q code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ASTRAI_API_KEY. Optional provider API keys may be forwarded through Astrai for model routing.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
