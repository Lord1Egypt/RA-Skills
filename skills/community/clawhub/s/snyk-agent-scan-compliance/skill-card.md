## Description: <br>
Helps agents edit skill documentation so snyk-agent-scan alerts for W001, W011, and W012 are resolved by restructuring content without suppressing useful information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill when authoring or editing agent skills, triaging local or CI snyk-agent-scan failures, and remediating W001, W011, and W012 alerts without removing useful documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated edits or scanner commands can change skill documentation or CI behavior. <br>
Mitigation: Review diffs before committing and rerun snyk-agent-scan to confirm the intended alerts are resolved. <br>
Risk: The scanner requires SNYK_TOKEN, and mishandled tokens could expose credentials. <br>
Mitigation: Provide SNYK_TOKEN only through environment variables or CI secrets; do not write tokens into skill files. <br>
Risk: Using floating scanner versions can make scan behavior less reproducible. <br>
Mitigation: Prefer pinned scanner versions when reproducible local or CI results matter. <br>


## Reference(s): <br>
- [W001 Prompt Injection Patterns](references/w001-patterns.md) <br>
- [W011 Third-Party Content Exposure Patterns](references/w011-patterns.md) <br>
- [W012 External URL and Version Pinning Patterns](references/w012-patterns.md) <br>
- [cc-skills Repository](https://github.com/samber/cc-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with inline code blocks and patch-oriented editing guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file edits and scanner commands; review diffs and scan results before relying on changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
