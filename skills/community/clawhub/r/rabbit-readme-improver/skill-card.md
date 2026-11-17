## Description:

Draft a new README.md, or audit and improve an existing one, using patterns measured from 100 real, currently-trending GitHub repos rather than generic advice, and written in the user's own saved voice rather than a generated open-source register.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whit3rabbit](https://clawhub.ai/user/whit3rabbit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to draft, audit, restructure, or polish project README files with measured open-source README conventions and optional saved voice profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional model-rewrite mode can send draft excerpts and a Rabbit model API key to a repository-selected endpoint.

Mitigation: Use --model-plan for a no-send preview, inspect .rabbit-model before --apply-model in untrusted repositories, or pass a known endpoint explicitly.

Risk: The skill reads project documentation and voice-profile files and can edit README text when asked.

Mitigation: Review proposed README changes before applying them and run the bundled checker or a normal diff review before publishing.

Risk: RABBIT_* environment variables may expose credentials to untrusted checkouts when optional model rewrite mode is used.

Mitigation: Keep valuable API keys out of RABBIT_* variables in untrusted repositories and use limited-scope keys for configured model endpoints.

## Reference(s):

- [README Pattern Reference](references/patterns.md)
- [README Checklist](references/checklist.md)
- [Craft Rules](references/craft.md)
- [STE Readability Reference](references/ste.md)
- [ClawHub Skill Page](https://clawhub.ai/whit3rabbit/skills/rabbit-readme-improver)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, README drafts or edits, review findings, inline shell commands, and optional JSON or SARIF reports from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3. Optional model rewrite mode may use RABBIT_MODEL_API_KEY, RABBIT_MODEL_BASE_URL, and RABBIT_MODEL_NAME when explicitly configured.]

## Skill Version(s):

0.5.0 (source: frontmatter metadata and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
