## Description:

pyscripts-org helps agents organize terminal Python scripts by requiring end-of-file summary blocks, generating script documentation, and maintaining a pitfall log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaibazax-dev](https://clawhub.ai/user/kaibazax-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage reusable Python utility scripts: check script documentation before adding new scripts, run or adapt existing scripts when appropriate, update summaries, and record recurring errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact documentation and bundled summary script describe different summary markers and documentation filenames, so generated documentation may be incomplete or unexpectedly named.

Mitigation: Review generated documentation before committing it and align the marker format and output filename before relying on the generated index.

Risk: Pitfall notes may capture secrets, local paths, or sensitive error details.

Mitigation: Redact sensitive values from pitfall entries before committing, sharing, or publishing them.

Risk: The workflow can encourage running existing local Python scripts, which may execute arbitrary local code.

Mitigation: Inspect scripts and understand their side effects before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaibazax-dev/skills/pyscripts-org)
- [Publisher profile](https://clawhub.ai/user/kaibazax-dev)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown documentation, Python code changes, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update script documentation and pitfall notes in the working directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
