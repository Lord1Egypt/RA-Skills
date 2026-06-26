## Description: <br>
Execution-based verification guardrail with 14 check items for AI agent output <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reikys](https://clawhub.ai/user/reikys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run a structured hallucination check on generated work, including file paths, commands, code syntax, completeness, consistency, dependencies, URLs, and source-backed claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local verification commands can inspect more files than intended when the target or scope is unclear. <br>
Mitigation: Run the skill manually with an explicit target path and scope before allowing any check to execute. <br>
Risk: Network checks can contact external URLs or internal endpoints from the user's environment. <br>
Mitigation: Review URLs first and require approval before running network checks. <br>
Risk: The auto-run prompt asks the agent to fix failed items, which could lead to unintended file changes. <br>
Mitigation: Avoid global auto-run use and require human review before applying fixes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/reikys/reikys-hallucination-guard) <br>
- [Python ast module documentation](https://docs.python.org/3/library/ast.html) <br>
- [npm registry API](https://registry.npmjs.org/) <br>
- [PyPI JSON API](https://pypi.org/pypi/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown PASS/FAIL report with command snippets and optional JSON summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include local and network verification commands; target and scope should be explicit.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
