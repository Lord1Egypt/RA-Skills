## Description: <br>
Multi-agent adversarial security review: three AI agents debate each finding so only real vulnerabilities remain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Har1sh-k](https://clawhub.ai/user/Har1sh-k) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to run AI-assisted security reviews for pull requests, diffs, commit ranges, or full repositories and to generate reports for local review or CI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target code, diffs, and repository context may be shared with external AI providers. <br>
Mitigation: Use the skill only on repositories and changes you are authorized to share with the selected providers. <br>
Risk: Provider API keys, GitHub tokens, cache files, auth files, debug traces, or reports may contain sensitive information. <br>
Mitigation: Use least-privilege credentials, avoid debug output on sensitive repositories unless needed, and review generated files before sharing or retaining them. <br>
Risk: AI-assisted findings may include false positives or miss subtle vulnerabilities. <br>
Mitigation: Treat output as security review guidance and validate findings with human review, testing, and formal audit processes where required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Har1sh-k/xfire-security-review) <br>
- [xfire GitHub repository](https://github.com/Har1sh-k/xfire) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and configuration examples; xfire can emit Markdown, JSON, or SARIF reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write reports, cache/auth files, debug traces, or GitHub PR comments when configured.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
