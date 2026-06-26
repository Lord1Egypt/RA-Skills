## Description: <br>
Scaffold a digital twin persona directory with markdown templates such as profile, state, persona examples, and guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xming521](https://clawhub.ai/user/xming521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to initialize or refresh local persona files for a digital twin workflow before filling in profile, state, examples, and guardrail templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated persona markdown may contain private personal data. <br>
Mitigation: Keep generated files local, omit credentials and unnecessary third-party details, and review content before sharing or committing it. <br>
Risk: Using overwrite mode can replace existing persona files. <br>
Mitigation: Choose the target directory carefully and use --force only when replacement is intended. <br>
Risk: The bundled guardrail template permits unsafe content when explicitly requested, while still requiring human approval. <br>
Mitigation: Review and tighten that template line before using the persona pack in workflows that should refuse unsafe content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xming521/weclone-init-twin) <br>
- [Publisher profile](https://clawhub.ai/user/xming521) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance, files] <br>
**Output Format:** [Markdown setup handoff plus generated markdown template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates profile, state, persona example, and guardrail templates in English or Chinese.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
