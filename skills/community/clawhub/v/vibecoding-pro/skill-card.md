## Description:

Vibecoding Pro helps developers run Generator-Evaluator loops that separate code generation from independent browser, API, or content evaluation for AI-assisted development workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to structure AI-assisted coding work as an iterative build-and-evaluate loop, especially for interactive UI, API, and documentation tasks that need observable acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evaluator loops that use browser or API tools can interact with live systems if configured with production URLs or credentials.

Mitigation: Run browser and API evaluation only against localhost, staging, or disposable test systems with non-production credentials.

Risk: Adapted generator or evaluator code may be given authority to write code, call authenticated APIs, or submit forms.

Mitigation: Review adapted code and agent permissions before enabling write access, authenticated API calls, or form submission.

## Reference(s):

- [Architecture Reference](references/architecture.md)
- [Evaluator Prompt Templates](references/evaluator-prompts.md)
- [Anthropic Engineering: Harness Design for Long-Running Application Development](https://www.anthropic.com/engineering/harness-design-long-running-apps)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with prompt templates, JSON schemas, Python code, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes evaluator scoring rubrics, loop-control guidance, and adaptable Python templates.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
