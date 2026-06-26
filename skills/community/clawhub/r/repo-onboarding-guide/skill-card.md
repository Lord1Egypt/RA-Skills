## Description: <br>
Scans repository directories and documentation to generate onboarding paths, recommended reading order, and common pitfalls for new team members. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to scan a repository locally and produce a reviewable onboarding guide for new contributors. The guide covers repository overview, first-read recommendations, key directories, setup notes, common pitfalls, and missing documentation suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script can perform broader repository audits and sensitive pattern scanning beyond a narrow onboarding guide. <br>
Mitigation: Review the skill before installing, run it only on approved repositories, and prefer narrowly scoped input paths or dry-run mode. <br>
Risk: Repository scans may expose sensitive filenames, documentation excerpts, or private project details in generated output. <br>
Mitigation: Avoid sensitive private repositories unless outputs are controlled, redact inputs when needed, and review generated Markdown or JSON before sharing. <br>
Risk: File access, shell execution, output locations, and redaction behavior may not be fully documented by the publisher. <br>
Mitigation: Inspect the bundled documentation and script behavior before use, and choose explicit output paths that remain local and reviewable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/repo-onboarding-guide) <br>
- [Skill routing and operating rules](artifact/SKILL.md) <br>
- [User documentation](artifact/README.md) <br>
- [Structured output specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>
- [Smoke test](artifact/tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Files, JSON] <br>
**Output Format:** [Markdown or JSON, optionally written to a local output file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local repository path as input and supports optional format, limit, output, and dry-run parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
