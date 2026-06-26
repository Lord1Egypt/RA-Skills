## Description: <br>
Reviews shell command text, scripts, or folders before execution to identify risky patterns such as pipe-to-shell, destructive deletes, dangerous redirection, obfuscated execution, and secret-like snippets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security reviewers use this skill to audit shell commands, scripts, or narrow folders before execution. It produces a structured review with dangerous patterns, medium-risk patterns, background notes, safer alternatives, manual confirmation items, and a final recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may include local paths or matched command snippets from user-provided inputs. <br>
Mitigation: Review generated reports before sharing and redact sensitive paths, secrets, or private command context. <br>
Risk: The skill's findings are advisory and may miss context-specific hazards in destructive commands or production changes. <br>
Mitigation: Keep human approval for destructive commands, permission changes, redirects, package install scripts, and production operations. <br>
Risk: Broad folder scans can expose more local material than intended in the review output. <br>
Mitigation: Use the skill on specific command text, scripts, or narrowly scoped folders. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/run-command-safety-check) <br>
- [Publisher Profile](https://clawhub.ai/user/52YuanChangXing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, files] <br>
**Output Format:** [Markdown or JSON safety review report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local report file when an output path is provided; otherwise returns the report to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
