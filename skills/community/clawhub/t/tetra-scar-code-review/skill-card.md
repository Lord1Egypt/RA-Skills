## Description: <br>
Tetra Scar Code Review helps agents and developers review code with checklist heuristics and reusable scar patterns that flag repeated review misses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aibenyclaude-coder](https://clawhub.ai/user/aibenyclaude-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to run local code-review checks across security, performance, correctness, and maintainability, then record missed findings as scar patterns so similar future diffs can be blocked early. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review scar records may contain sensitive incident details or secret-like patterns if users paste them into descriptions. <br>
Mitigation: Keep review_scars.jsonl under local control and avoid storing real secrets in scar descriptions or regex patterns. <br>
Risk: Broad scar regexes can block unrelated changes, especially when used in CI. <br>
Mitigation: Review and narrow scar patterns before enabling them as blocking checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aibenyclaude-coder/tetra-scar-code-review) <br>
- [Publisher profile](https://clawhub.ai/user/aibenyclaude-coder) <br>
- [Tetra Genesis project](https://github.com/b-button-corp/tetra-genesis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands, Python snippets, and JSONL scar records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can produce local review findings, diff block messages, and review_scars.jsonl entries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
